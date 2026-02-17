"""
AI Textbook RAG API - Main FastAPI Application
"""

import os
import warnings
import json
import re
from typing import List, Optional

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    import google.generativeai as genai

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from pgvector.psycopg2 import register_vector

from src.api.logging_config import log
from src.api.fast_embeddings import generate_fast_embedding

# Load environment variables
load_dotenv()

# --- Globals ---
neon_conn = None


# --- Pydantic Models ---
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# --- Environment and Model Configuration ---
def load_environment():
    """Loads environment variables and configures necessary clients."""
    global neon_conn
    # Configure Google AI
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or "YOUR_GOOGLE_API_KEY" in api_key:
        log.warning("GOOGLE_API_KEY not found or is a placeholder in the .env file.")
    else:
        try:
            genai.configure(api_key=api_key)
            log.info("Google GenAI Client initialized.")
        except Exception as e:
            log.error(f"Failed to configure Google GenAI Client: {e}", exc_info=True)

    # Configure Neon DB Connection
    neon_db_url = os.getenv("NEON_DB_KEY")
    if not neon_db_url:
        log.warning("NEON_DB_KEY not found in .env file.")
    else:
        try:
            neon_conn = psycopg2.connect(neon_db_url)
            with neon_conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                register_vector(neon_conn)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS textbook_content (
                        id SERIAL PRIMARY KEY,
                        source_file TEXT,
                        chapter TEXT,
                        section TEXT,
                        content TEXT,
                        embedding VECTOR(384)
                    );
                """)
            neon_conn.commit()
            log.info("Database table 'textbook_content' is set up.")
        except Exception as e:
            log.error(f"Failed to connect to database or setup table: {e}", exc_info=True)

    # Only populate database, don't reset on every startup
    populate_database()


def populate_database():
    """Populates the database with textbook content."""
    if not neon_conn:
        log.error("Cannot populate database without a connection.")
        return

    try:
        with neon_conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM textbook_content;")
            count = cur.fetchone()[0]
            if count > 0:
                log.info(f"Database already populated with {count} records. Skipping.")
                return

        log.info("Populating database with textbook content...")
        # Navigate to the docs directory (5 levels up from src/api to reach project root)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, "..", "..", "..", "..", ".."))
        docs_dir = os.path.join(project_root, "frontend", "docusaurus-app", "docs")

        log.info(f"Looking for docs at: {docs_dir}")
        
        if not os.path.exists(docs_dir):
            log.error(f"Docs directory not found: {docs_dir}")
            return

        doc_files = [os.path.join(docs_dir, f) for f in os.listdir(docs_dir) if f.endswith(".md")]
        log.info(f"Found {len(doc_files)} markdown files: {[os.path.basename(f) for f in doc_files]}")

        records_added = 0
        for doc_file in doc_files:
            log.info(f"Processing: {os.path.basename(doc_file)}")
            with open(doc_file, "r", encoding="utf-8") as f:
                content = f.read()

            file_name = os.path.basename(doc_file)
            chapter_title = "General Content"
            chapter_match = re.search(r"^#\s*(.*)", content, re.MULTILINE)
            if chapter_match:
                chapter_title = chapter_match.group(1).strip()

            parts = re.split(r"(^##\s*.*)", content, flags=re.MULTILINE)
            current_section_title = "Introduction"
            for part in parts:
                if not part.strip():
                    continue
                section_match = re.match(r"^##\s*(.*)", part, re.MULTILINE)
                if section_match:
                    current_section_title = section_match.group(1).strip()
                else:
                    chunks = part.split("\n\n")
                    for chunk in chunks:
                        chunk_stripped = chunk.strip()
                        if len(chunk_stripped) > 50:
                            try:
                                embedding = generate_fast_embedding(chunk_stripped, "retrieval_document")
                                formatted_embedding = [float(x) for x in embedding]
                                with neon_conn.cursor() as cur:
                                    cur.execute(
                                        """
                                        INSERT INTO textbook_content (source_file, chapter, section, content, embedding)
                                        VALUES (%s, %s, %s, %s, %s);
                                        """,
                                        (file_name, chapter_title, current_section_title, chunk_stripped, formatted_embedding)
                                    )
                                neon_conn.commit()
                                records_added += 1
                            except Exception as e:
                                log.error(f"Error processing chunk: {e}")
        
        log.info(f"Finished populating database. Added {records_added} records.")
    except Exception as e:
        log.error(f"Error populating database: {e}", exc_info=True)


def reset_database():
    """Resets the database by dropping and recreating the table."""
    if not neon_conn:
        log.error("Cannot reset database without a connection.")
        return

    try:
        with neon_conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS textbook_content CASCADE;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS textbook_content (
                    id SERIAL PRIMARY KEY,
                    source_file TEXT,
                    chapter TEXT,
                    section TEXT,
                    content TEXT,
                    embedding VECTOR(384)
                );
            """)
        neon_conn.commit()
        log.info("Database table 'textbook_content' has been reset.")
    except Exception as e:
        log.error(f"Error resetting database: {e}", exc_info=True)


# --- FastAPI App Setup ---
app = FastAPI(
    title="AI Textbook RAG API",
    description="An API for interacting with the AI Textbook using a RAG pipeline with Neon.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Root endpoint to confirm the API is running."""
    return {
        "message": "AI Textbook RAG API is running!",
        "endpoints": {
            "/docs": "API documentation",
            "/ask": "Chat endpoint for asking questions"
        },
        "status": "healthy"
    }


# Configure CORS
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Lifecycle Events ---
@app.on_event("startup")
def startup_event():
    """Sets up the database at startup."""
    load_environment()


@app.on_event("shutdown")
def shutdown_event():
    """Close the database connection when shutting down."""
    global neon_conn
    if neon_conn:
        neon_conn.close()


@app.post("/ask", summary="Ask a Question (RAG)")
def ask(request: ChatRequest):
    """Handles a user's question using a RAG pipeline with Neon."""
    if not neon_conn:
        raise HTTPException(status_code=503, detail="Database connection not available.")

    last_user_message = next((msg.content for msg in reversed(request.messages) if msg.role == "user" and msg.content.strip()), None)
    if not last_user_message:
        raise HTTPException(status_code=400, detail="No user message with content found.")

    query_embedding = generate_fast_embedding(last_user_message, "retrieval_query")

    try:
        # Convert the embedding to the proper format for pgvector
        formatted_embedding = [float(x) for x in query_embedding]

        with neon_conn.cursor() as cur:
            cur.execute(
                "SELECT content, chapter, section FROM textbook_content ORDER BY embedding <-> %s::VECTOR LIMIT 3;",
                (formatted_embedding,)
            )
            search_results = cur.fetchall()

        # Check if we got results
        if not search_results:
            log.warning("No relevant content found in database for the query")
            # Return a default response if no context is found
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"You are a helpful AI assistant. The user asked: '{last_user_message}'. Unfortunately, I couldn't find relevant information in the textbook to answer this question."
            response = model.generate_content(prompt)
            final_answer = f"{response.text}\n\nNote: No relevant sources were found in the textbook."
            return {"answer": final_answer}

        context_parts = [res[0] for res in search_results]
        citations = [f"Source: {res[1]} - {res[2]}" for res in search_results]
        context = "\n---\n".join(context_parts)
        unique_citations = "\n".join(sorted(list(set(citations))))

        conversation_history = "\n".join([f"{msg.role.capitalize()}: {msg.content}" for msg in request.messages])
        prompt = f"You are a helpful AI assistant. Answer the user's question based on the provided context.\n\nContext:\n{context}\n\nConversation History:\n{conversation_history}\n\nAnswer:"

        # Use gemini-2.5-flash model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        # Check if response has text
        if hasattr(response, 'text') and response.text:
            final_answer = f"{response.text}\n\n--- Sources ---\n{unique_citations}"
        else:
            final_answer = f"I'm sorry, but I couldn't generate a response for your query: '{last_user_message}'\n\n--- Sources ---\n{unique_citations}"

        return {"answer": final_answer}
    except Exception as e:
        log.error(f"Error processing RAG request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate an answer.")


# --- Main execution ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    log.info(f"Starting FastAPI server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
