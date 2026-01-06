import os
import re
import uuid
import time
import google.generativeai as genai
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from logging_config import log
from fast_embeddings import generate_fast_embeddings_batch

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

EMBEDDING_DIMENSION = get_embedding_dimension()

def load_environment():
    """Loads environment variables and returns a configured GenAI client."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not found in .env file.")
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    
    genai.configure(api_key=api_key)
    log.info("Google GenAI Client initialized.")
    
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    if not qdrant_url or not qdrant_api_key:
        log.error("Qdrant credentials not found in .env file.")
        raise ValueError("Qdrant credentials not found.")
        
    return qdrant_url, qdrant_api_key

def process_and_chunk_content(text_content, all_chunks_list, file_name, chapter, section):
    """Helper function to chunk content and add it to a list with metadata."""
    chunks = text_content.split("\n\n")
    for i, chunk in enumerate(chunks):
        chunk_stripped = chunk.strip()
        if len(chunk_stripped) > 50:
            all_chunks_list.append({
                "content": chunk_stripped,
                "metadata": {
                    "source_file": file_name,
                    "chapter": chapter,
                    "section": section,
                    "chunk_number": i
                }
            })
    log.info(f"Processed {len(chunks)} chunks for section '{section}' in chapter '{chapter}'.")

def ingest_docs():
    """Reads markdown files, extracts structured content, and splits it into chunks."""
    log.info("Starting document ingestion process...")
    # ... (rest of function is identical)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../.."))
    docs_dir = os.path.join(project_root, "frontend", "docusaurus-app", "docs")
    log.info(f"Target docs directory: {docs_dir}")
    doc_files_relative = ["intro.md", "chapter1.md", "chapter2.md", "chapter3.md", "chapter4.md", "chapter5.md", "chapter6.md", "chapter7.md"]
    doc_files = [os.path.join(docs_dir, f) for f in doc_files_relative]
    all_chunks_with_metadata = []
    for doc_file in doc_files:
        try:
            with open(doc_file, "r", encoding="utf-8") as f:
                content = f.read()
            log.info(f"Successfully read file: {doc_file}")
        except FileNotFoundError:
            log.error(f"File not found: {doc_file}. Skipping.")
            continue
        file_name = os.path.basename(doc_file)
        chapter_title = "General Content"
        chapter_match = re.search(r"^#\s*(.*)", content, re.MULTILINE)
        if chapter_match:
            chapter_title = chapter_match.group(1).strip()
            content = re.sub(r"^#\s*(.*)", "", content, 1, re.MULTILINE).strip()
        parts = re.split(r"(^##\s*.*)", content, flags=re.MULTILINE)
        current_section_title = "Introduction"
        current_section_content = []
        for part in parts:
            if not part.strip(): continue
            section_match = re.match(r"^##\s*(.*)", part, re.MULTILINE)
            if section_match:
                if current_section_content:
                    process_and_chunk_content("".join(current_section_content), all_chunks_with_metadata, file_name, chapter_title, current_section_title)
                current_section_title = section_match.group(1).strip()
                current_section_content = []
            else:
                current_section_content.append(part)
        if current_section_content:
            process_and_chunk_content("".join(current_section_content), all_chunks_with_metadata, file_name, chapter_title, current_section_title)
    log.info(f"Completed ingestion. Found {len(all_chunks_with_metadata)} total chunks.")
    return all_chunks_with_metadata

def main():
    """Main execution function for the ingestion script."""
    try:
        qdrant_url, qdrant_api_key = load_environment()
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        log.info("Qdrant client initialized.")

        try:
            collections_response = qdrant_client.get_collections()
            existing_collections = [col.name for col in collections_response.collections]
            log.info(f"Found existing Qdrant collections: {existing_collections}")

            if COLLECTION_NAME not in existing_collections:
                log.info(f"Collection '{COLLECTION_NAME}' not found. Creating it now...")
                qdrant_client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=models.VectorParams(size=EMBEDDING_DIMENSION, distance=models.Distance.COSINE),
                )
                log.info(f"Successfully created collection '{COLLECTION_NAME}'.")
            else:
                log.info(f"Collection '{COLLECTION_NAME}' already exists. Skipping creation.")
        except Exception as e:
            log.error(f"Failed to check or create Qdrant collection: {e}", exc_info=True)
            # Depending on the desired behavior, you might want to exit here.
            # For now, we'll let it proceed, but upsert might fail.
            pass

        chunks_with_metadata = ingest_docs()
        if not chunks_with_metadata:
            log.warning("No chunks were ingested. Aborting.")
            return

        batch_size = 20  # Reduced batch size to be safer
        batches = [chunks_with_metadata[i:i + batch_size] for i in range(0, len(chunks_with_metadata), batch_size)]
        log.info(f"Created {len(batches)} batches of size {batch_size}.")

        total_points_upserted = 0
        for i, batch in enumerate(batches):
            log.info(f"Processing batch {i+1}/{len(batches)}...")
            contents_to_embed = [item['content'] for item in batch]
            
            try:
                use_fast_embeddings = os.getenv("USE_FAST_EMBEDDINGS", "false").lower() == "true"

                if use_fast_embeddings:
                    log.info("Generating fast embeddings for the batch...")
                    embeddings = generate_fast_embeddings_batch(contents_to_embed, "retrieval_document")
                    log.info(f"Successfully generated {len(embeddings)} fast embeddings for this batch.")
                else:
                    log.info("Generating Google API embeddings for the batch...")
                    result = genai.embed_content(
                        model=EMBEDDING_MODEL,
                        content=contents_to_embed,
                        task_type="retrieval_document"
                    )
                    embeddings = result['embedding']
                    log.info(f"Successfully generated {len(embeddings)} Google API embeddings for this batch.")

                if len(embeddings) != len(batch):
                    log.error(f"Mismatch in batch {i+1}: {len(batch)} chunks vs {len(embeddings)} embeddings. Skipping.")
                    continue

                points = [
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embeddings[j],
                        payload={**item['metadata'], "content": item['content']}
                    ) for j, item in enumerate(batch)
                ]

                qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
                total_points_upserted += len(points)
                log.info(f"Upserted {len(points)} points for batch {i+1}.")

            except Exception as e:
                log.error(f"Failed to process batch {i+1}: {e}", exc_info=True)

            if i < len(batches) - 1:
                log.info("Waiting for 60 seconds to respect API rate limits...")
                time.sleep(60)

        log.info(f"--- Finished ingestion. Successfully upserted {total_points_upserted} total points to Qdrant. ---")

    except Exception as e:
        log.critical(f"A critical error occurred during the ingestion process: {e}", exc_info=True)

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
