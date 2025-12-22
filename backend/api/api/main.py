import os
import google.genai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from qdrant_client import QdrantClient

from logging_config import log

# --- Constants ---
COLLECTION_NAME = "ai_textbook"
EMBEDDING_MODEL = "models/embedding-001"

# --- Globals ---
qdrant_client = None
genai_client = None

# --- Environment and Model Configuration ---

def load_environment():
    """Loads environment variables and configures necessary clients."""
    global qdrant_client, genai_client
    load_dotenv()
    
    # Configure Google AI
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not found in .env file.")
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    genai_client = genai.Client(api_key=api_key)
    log.info("Google GenAI Client initialized.")
    
    # Configure Qdrant Client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    if not qdrant_url or not qdrant_api_key:
        log.error("QDRANT_URL or QDRANT_API_KEY not found in .env file.")
        raise ValueError("Qdrant credentials not found.")
    
    try:
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        qdrant_client.get_collection(collection_name=COLLECTION_NAME) # Health check
        log.info("Qdrant client initialized and connected successfully.")
    except Exception as e:
        log.critical(f"Failed to connect to Qdrant: {e}", exc_info=True)
        qdrant_client = None


# --- FastAPI App Setup ---
app = FastAPI(
    title="AI Textbook RAG API",
    description="An API for interacting with the AI Textbook using a RAG pipeline.",
    version="1.0.0"
)

allowed_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

class ExplainRequest(BaseModel):
    text_selection: str

# --- Helper Functions ---
def generate_embedding(text: str, task_type: str) -> list[float]:
    """Generates an embedding for a given text."""
    if not genai_client:
        raise HTTPException(status_code=500, detail="Google AI Client not initialized.")
    try:
        result = genai_client.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type=task_type,
            title="AI Textbook"
        )
        log.info(f"Successfully generated embedding for task type: {task_type}")
        return result['embedding']
    except Exception as e:
        log.error(f"Failed to generate embedding: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating text embedding.")

# --- Lifecycle Events ---
@app.on_event("startup")
def startup_event():
    """Loads the environment and initializes clients at startup."""
    load_environment()

# --- API Endpoints ---
@app.get("/", summary="Root Endpoint")
def read_root():
    return {"message": "Welcome to the RAG Chatbot API"}

@app.get("/health", summary="Health Check")
def health_check():
    qdrant_ok = False
    if qdrant_client:
        try:
            qdrant_client.get_collection(collection_name=COLLECTION_NAME)
            qdrant_ok = True
        except Exception:
            qdrant_ok = False
    return {"status": "ok", "qdrant_connected": qdrant_ok, "genai_client_initialized": genai_client is not None}

@app.post("/explain_text", summary="Explain Text Selection")
def explain_text(request: ExplainRequest):
    if not genai_client:
        raise HTTPException(status_code=500, detail="Google AI Client not initialized.")
    prompt = f"You are an expert in the subject matter of the AI Textbook. " \
             f"Explain the following text selection clearly and concisely:\n\n" \
             f"Text Selection: {request.text_selection}\n\n" \
             f"Explanation:"
    try:
        model = genai_client.get_generative_model('gemini-pro')
        response = model.generate_content(prompt)
        return {"explanation": response.text}
    except Exception as e:
        log.error(f"Error in /explain_text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate explanation.")


@app.post("/ask", summary="Ask a Question (RAG)")
def ask(request: ChatRequest):
    """Handles a user's question using a RAG pipeline with Qdrant."""
    if not qdrant_client or not genai_client:
        log.error("Attempted to call /ask but a client is not available.")
        raise HTTPException(status_code=503, detail="A backend client is not available.")

    last_user_message = next((msg.content for msg in reversed(request.messages) if msg.role == "user" and msg.content.strip()), None)
    if not last_user_message:
        raise HTTPException(status_code=400, detail="No user message with content found.")

    log.info(f"Processing RAG request for query: '{last_user_message[:50]}...'")

    query_embedding = generate_embedding(last_user_message, "RETRIEVAL_QUERY")

    try:
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3,
            with_payload=True
        )
        log.info(f"Found {len(search_results)} relevant documents in Qdrant.")
    except Exception as e:
        log.error(f"Qdrant search failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error searching the vector database.")

    context_parts = [hit.payload.get('content', 'N/A') for hit in search_results]
    citations = [f"Source: {hit.payload.get('chapter', 'N/A')} - {hit.payload.get('section', 'N/A')}" for hit in search_results]
    context = "\n---\n".join(context_parts)
    unique_citations = "\n".join(sorted(list(set(citations))))

    conversation_history = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in request.messages[:-1]])

    prompt = f"You are a helpful and professional AI assistant. " \
             f"You will answer the user's question based on the provided context. " \
             f"If you cannot find the answer in the context, state that you don't know, " \
             f"rather than making up an answer. " \
             f"At the end of your answer, include citations from the provided sources in a '--- Sources ---' section.\n\n" \
             f"Conversation History:\n{conversation_history}\n\n" \
             f"Context:\n{context}\n\n" \
             f"User Question: {last_user_message}\n\n" \
             f"Answer:"

    try:
        model = genai_client.get_generative_model('gemini-pro')
        response = model.generate_content(prompt)
        final_answer = f"{response.text}\n\n--- Sources ---\n{unique_citations}"
        log.info("Successfully generated RAG answer.")
        return {"answer": final_answer}
    except Exception as e:
        log.error(f"Error generating RAG answer from Gemini: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate an answer.")

