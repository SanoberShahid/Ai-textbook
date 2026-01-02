import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from qdrant_client import QdrantClient, models

from logging_config import log
from fast_embeddings import generate_fast_embedding, generate_fast_embeddings_batch

# --- Constants ---
COLLECTION_NAME = "ai_textbook"
EMBEDDING_MODEL = "models/embedding-001"

# Determine embedding dimension based on configuration
def get_embedding_dimension():
    use_fast_embeddings = os.getenv("USE_FAST_EMBEDDINGS", "false").lower() == "true"
    if use_fast_embeddings:
        from config import embedding_config
        return embedding_config.get_embedding_dimension()
    else:
        # Google's embedding-001 model produces 768-dimensional embeddings
        return 768

# --- Globals ---
qdrant_client = None
qdrant_local_mode = False  # Flag to indicate if using local in-memory Qdrant

# --- Environment and Model Configuration ---

def load_environment():
    """Loads environment variables and configures necessary clients."""
    global qdrant_client, qdrant_local_mode
    load_dotenv()

    # Configure Google AI
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or "YOUR_GOOGLE_API_KEY" in api_key:
        log.error("GOOGLE_API_KEY not found or is a placeholder in the .env file.")
        # We don't raise here to allow the server to start, but dependent endpoints will fail.
    else:
        try:
            genai.configure(api_key=api_key)
            log.info("Google GenAI Client initialized.")
        except Exception as e:
            log.error(f"Failed to configure Google GenAI Client: {e}", exc_info=True)


    # Configure Qdrant Client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key or "YOUR_QDRANT_API_KEY" in qdrant_api_key:
        log.warning("QDRANT_URL or QDRANT_API_KEY are missing or placeholders in the .env file.")
        log.warning("Attempting to initialize in-memory Qdrant for development...")
        try:
            qdrant_client = QdrantClient(":memory:")  # In-memory mode
            qdrant_local_mode = True
            # Create collection in memory
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=get_embedding_dimension(), distance=models.Distance.COSINE),
            )
            log.info("In-memory Qdrant client initialized successfully.")
        except Exception as e:
            log.error(f"Failed to initialize in-memory Qdrant: {e}", exc_info=True)
            qdrant_client = None
        return

    try:
        log.info(f"Attempting to connect to Qdrant at {qdrant_url}...")
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        qdrant_client.get_collection(collection_name=COLLECTION_NAME) # Health check
        log.info("Qdrant client initialized and connected successfully.")
    except Exception as e:
        log.warning(f"Failed to connect to external Qdrant server: {e}", exc_info=True)
        # Check the error message for common issues
        error_str = str(e).lower()
        if "401" in error_str or "unauthorized" in error_str:
            log.error("QDRANT CONNECTION FAILED: Authentication error (401). Please check your QDRANT_API_KEY in the .env file.")
        elif "404" in error_str or "not found" in error_str:
            log.error(f"QDRANT CONNECTION FAILED: Collection '{COLLECTION_NAME}' not found (404). Please ensure the collection exists.")
        elif "connection failed" in error_str or "network is unreachable" in error_str:
             log.error("QDRANT CONNECTION FAILED: Could not connect to the Qdrant server. Please check the QDRANT_URL and your network connection.")
        else:
            log.error("QDRANT CONNECTION FAILED: An unknown error occurred. See the traceback above for details.")

        # Try to initialize in-memory Qdrant as fallback
        log.info("Attempting to initialize in-memory Qdrant as fallback...")
        try:
            qdrant_client = QdrantClient(":memory:")  # In-memory mode
            qdrant_local_mode = True
            # Create collection in memory
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=get_embedding_dimension(), distance=models.Distance.COSINE),
            )
            log.info("In-memory Qdrant client initialized successfully as fallback.")
        except Exception as mem_e:
            log.error(f"Failed to initialize in-memory Qdrant fallback: {mem_e}", exc_info=True)
            qdrant_client = None


# --- FastAPI App Setup ---
app = FastAPI(
    title="AI Textbook RAG API",
    description="An API for interacting with the AI Textbook using a RAG pipeline.",
    version="1.0.0"
)

# Allow all origins during development
allowed_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002")  # Common Docusaurus ports
if allowed_origins_str.strip() == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',')]

# Add the frontend URL to allowed origins
allowed_origins.extend([
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3000/my-ai-textbook/",
    "http://localhost:3000/my-ai-textbook",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3000/my-ai-textbook/",
    "http://127.0.0.1:3000/my-ai-textbook"
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=".*",  # Allow any origin with regex
    # Additional options to handle preflight requests
    max_age=600,
)

# --- Pydantic Models ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

class ExplainRequest(BaseModel):
    text_selection: str

class QuizRequest(BaseModel):
    chapter_id: str


# --- Helper Functions ---
def generate_embedding(text: str, task_type: str) -> list[float]:
    """Generates an embedding for a given text using either fast local embeddings or Google API."""
    use_fast_embeddings = os.getenv("USE_FAST_EMBEDDINGS", "false").lower() == "true"

    if use_fast_embeddings:
        try:
            embedding = generate_fast_embedding(text, task_type)
            log.info(f"Successfully generated fast embedding for task type: {task_type}")
            return embedding
        except Exception as e:
            log.error(f"Failed to generate fast embedding: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error generating text embedding with fast embeddings.")
    else:
        try:
            result = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=text,
                task_type=task_type
            )
            log.info(f"Successfully generated Google API embedding for task type: {task_type}")
            return result['embedding']
        except Exception as e:
            log.error(f"Failed to generate Google API embedding: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error generating text embedding.")

def populate_qdrant_with_textbook_content():
    """Populate Qdrant with textbook content if in local mode."""
    global qdrant_client, qdrant_local_mode

    if not qdrant_local_mode or qdrant_client is None:
        log.info("Not in local mode or Qdrant client not available, skipping content population.")
        return

    log.info("Populating Qdrant with textbook content for local development...")

    import uuid
    import re
    import os

    # Load textbook content from docs directory
    # The path structure is: backend/api/api/main.py -> backend/api/api/ -> backend/api/ -> backend/ -> project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    docs_dir = os.path.join(project_root, "frontend", "docusaurus-app", "docs")
    log.info(f"Loading textbook content from: {docs_dir}")

    doc_files_relative = ["intro.md", "chapter1.md", "chapter2.md", "chapter3.md", "chapter4.md", "chapter5.md", "chapter6.md", "chapter7.md"]
    doc_files = [os.path.join(docs_dir, f) for f in doc_files_relative]

    all_chunks_with_metadata = []

    for doc_file in doc_files:
        try:
            with open(doc_file, "r", encoding="utf-8") as f:
                content = f.read()
            log.info(f"Successfully read file: {doc_file}")
        except FileNotFoundError:
            log.warning(f"File not found: {doc_file}. Skipping.")
            continue

        file_name = os.path.basename(doc_file)
        chapter_title = "General Content"

        # Extract chapter title from the first heading
        chapter_match = re.search(r"^#\s*(.*)", content, re.MULTILINE)
        if chapter_match:
            chapter_title = chapter_match.group(1).strip()
            content = re.sub(r"^#\s*(.*)", "", content, 1, re.MULTILINE).strip()

        # Split content by sections
        parts = re.split(r"(^##\s*.*)", content, flags=re.MULTILINE)
        current_section_title = "Introduction"
        current_section_content = []

        for part in parts:
            if not part.strip():
                continue
            section_match = re.match(r"^##\s*(.*)", part, re.MULTILINE)
            if section_match:
                if current_section_content:
                    # Process the previous section
                    chunks = current_section_content[0].split("\n\n")
                    for i, chunk in enumerate(chunks):
                        chunk_stripped = chunk.strip()
                        if len(chunk_stripped) > 50:  # Only include chunks with substantial content
                            all_chunks_with_metadata.append({
                                "content": chunk_stripped,
                                "metadata": {
                                    "source_file": file_name,
                                    "chapter": chapter_title,
                                    "section": current_section_title,
                                    "chunk_number": i
                                }
                            })
                current_section_title = section_match.group(1).strip()
                current_section_content = [part]
            else:
                current_section_content.append(part)

        # Process the last section
        if current_section_content:
            full_content = "".join(current_section_content)
            chunks = full_content.split("\n\n")
            for i, chunk in enumerate(chunks):
                chunk_stripped = chunk.strip()
                if len(chunk_stripped) > 50:  # Only include chunks with substantial content
                    all_chunks_with_metadata.append({
                        "content": chunk_stripped,
                        "metadata": {
                            "source_file": file_name,
                            "chapter": chapter_title,
                            "section": current_section_title,
                            "chunk_number": i
                        }
                    })

    if not all_chunks_with_metadata:
        log.warning("No textbook content found to populate Qdrant.")
        return

    log.info(f"Found {len(all_chunks_with_metadata)} content chunks to add to Qdrant.")

    # Process in batches
    batch_size = 20
    batches = [all_chunks_with_metadata[i:i + batch_size] for i in range(0, len(all_chunks_with_metadata), batch_size)]
    log.info(f"Processing {len(batches)} batches of size up to {batch_size}.")

    total_points_upserted = 0

    for i, batch in enumerate(batches):
        log.info(f"Processing batch {i+1}/{len(batches)}...")
        contents_to_embed = [item['content'] for item in batch]

        try:
            # Generate embeddings for the batch
            from fast_embeddings import generate_fast_embeddings_batch
            log.info(f"Generating embeddings for {len(contents_to_embed)} chunks...")
            embeddings = generate_fast_embeddings_batch(contents_to_embed, "retrieval_document")
            log.info(f"Successfully generated {len(embeddings)} embeddings for this batch.")

            if len(embeddings) != len(batch):
                log.error(f"Mismatch: {len(batch)} chunks vs {len(embeddings)} embeddings. Skipping.")
                continue

            # Create Qdrant points
            points = []
            for j, item in enumerate(batch):
                point = models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embeddings[j],
                    payload={**item['metadata'], "content": item['content']}
                )
                points.append(point)

            # Upload to Qdrant
            qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
            batch_count = len(points)
            total_points_upserted += batch_count
            log.info(f"Upserted {batch_count} points for batch {i+1}.")

        except Exception as e:
            log.error(f"Failed to process batch {i+1}: {e}", exc_info=True)

    # Verify the data was added
    count = qdrant_client.count(collection_name=COLLECTION_NAME)
    log.info(f"--- Finished populating Qdrant. Total points in collection: {count.count} ---")


# --- Lifecycle Events ---
@app.on_event("startup")
def startup_event():
    """Loads the environment and initializes clients at startup."""
    load_environment()

    # If in local mode, populate with textbook content
    if qdrant_local_mode and qdrant_client is not None:
        populate_qdrant_with_textbook_content()

# --- API Endpoints ---
@app.get("/", summary="Root Endpoint")
def read_root():
    return {"message": "Welcome to the RAG Chatbot API"}

@app.get("/health", summary="Health Check")
def health_check():
    qdrant_ok = False
    genai_ok = False
    if qdrant_client:
        try:
            qdrant_client.get_collection(collection_name=COLLECTION_NAME)
            qdrant_ok = True
        except Exception:
            qdrant_ok = False
    try:
        genai.get_model("models/embedding-001")
        genai_ok = True
    except Exception:
        genai_ok = False
    return {"status": "ok", "qdrant_connected": qdrant_ok, "genai_configured": genai_ok}

@app.post("/generate_quiz", summary="Generate a Quiz for a Chapter")
def generate_quiz_endpoint(request: QuizRequest):
    """Generates a multiple-choice quiz for a given chapter."""
    try:
        genai.get_model("models/embedding-001")
    except Exception:
        raise HTTPException(status_code=503, detail="Google AI Client not available.")

    # Convert "Chapter 1" to "chapter1.md"
    chapter_filename = request.chapter_id.replace(" ", "").lower() + ".md"
    
    # Build the path to the docs directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.abspath(os.path.join(script_dir, "../../../frontend/docusaurus-app/docs"))
    file_path = os.path.join(docs_dir, chapter_filename)

    log.info(f"Attempting to generate quiz for '{request.chapter_id}' from file: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        log.error(f"Chapter file not found at {file_path}")
        raise HTTPException(status_code=404, detail=f"Content for '{request.chapter_id}' not found.")

    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    Based on the following textbook chapter content, generate 3 multiple-choice questions.
    Each question must have 4 options, and you must clearly indicate the correct answer.
    Format the output as a valid JSON array of objects, where each object has:
    - "question": The question text (string).
    - "options": An array of 4 strings for the answer options.
    - "correctAnswer": The correct answer string, which must exactly match one of the options.

    Do not include any text or formatting outside of the JSON array itself.

    Chapter Content:
    {content[:4000]}

    Example of the required JSON output format:
    [
      {{
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Rome"],
        "correctAnswer": "Paris"
      }}
    ]

    Quiz Questions (JSON array only):
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean the response to extract only the JSON part
        json_text = response.text.strip()
        if json_text.startswith("```json"):
            json_text = json_text[7:-4].strip()

        quiz_data = json.loads(json_text)
        
        # Basic validation
        if not isinstance(quiz_data, list) or not all(isinstance(q, dict) and 'question' in q and 'options' in q and 'correctAnswer' in q for q in quiz_data):
            raise ValueError("Invalid JSON structure.")
        
        log.info(f"Successfully generated quiz for chapter '{request.chapter_id}'.")
        return {"quiz": quiz_data}

    except json.JSONDecodeError:
        log.error(f"Failed to decode JSON from model response: {response.text}")
        raise HTTPException(status_code=500, detail="Failed to generate a valid quiz (JSON decoding error).")
    except Exception as e:
        log.error(f"Error generating quiz from Gemini: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {e}")


@app.post("/explain_text", summary="Explain Text Selection")
def explain_text(request: ExplainRequest):
    try:
        genai.get_model("models/embedding-001")
    except Exception:
        raise HTTPException(status_code=500, detail="Google AI Client not initialized.")
    prompt = f"You are an expert in the subject matter of the AI Textbook. " \
             f"Explain the following text selection clearly and concisely:\n\n" \
             f"Text Selection: {request.text_selection}\n\n" \
             f"Explanation:"
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return {"explanation": response.text}
    except Exception as e:
        log.error(f"Error in /explain_text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate explanation.")


@app.post("/ask", summary="Ask a Question (RAG)")
def ask(request: ChatRequest):
    """Handles a user's question using a RAG pipeline with Qdrant."""
    if not qdrant_client:
        log.error("Attempted to call /ask but qdrant_client is not available.")
        raise HTTPException(status_code=503, detail="A backend client is not available.")
    try:
        genai.get_model("models/embedding-001")
    except Exception:
        raise HTTPException(status_code=503, detail="Google AI Client not available.")

    last_user_message = next((msg.content for msg in reversed(request.messages) if msg.role == "user" and msg.content.strip()), None)
    if not last_user_message:
        raise HTTPException(status_code=400, detail="No user message with content found.")

    log.info(f"Processing RAG request for query: '{last_user_message[:50]}...'")

    query_embedding = generate_embedding(last_user_message, "retrieval_query")

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

    # Check if search results exist and have content
    if search_results:
        context_parts = [hit.payload.get('content', 'N/A') for hit in search_results]
        citations = [f"Source: {hit.payload.get('chapter', 'N/A')} - {hit.payload.get('section', 'N/A')}" for hit in search_results]
        context = "\n---\n".join(context_parts)
        unique_citations = "\n".join(sorted(list(set(citations))))

        # Update the prompt to include context
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
    else:
        # No relevant context found, but still generate a response using the LLM
        log.warning("No relevant documents found in Qdrant for the query.")
        conversation_history = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in request.messages[:-1]])

        prompt = f"You are a helpful and professional AI assistant. " \
                 f"Answer the user's question to the best of your ability. " \
                 f"Conversation History:\n{conversation_history}\n\n" \
                 f"User Question: {last_user_message}\n\n" \
                 f"Answer:"

        # Set citations to empty for this case
        unique_citations = ""

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        if unique_citations:  # If there are citations, include them
            final_answer = f"{response.text}\n\n--- Sources ---\n{unique_citations}"
        else:  # If no citations, just return the response
            final_answer = response.text

        log.info("Successfully generated RAG answer.")
        return {"answer": final_answer}
    except Exception as e:
        log.error(f"Error generating RAG answer from Gemini: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate an answer.")

# --- Main execution ---
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    log.info(f"Starting FastAPI server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

