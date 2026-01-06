"""
Script to populate in-memory Qdrant with textbook content for development
"""

import os
import sys
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from fast_embeddings import generate_fast_embeddings_batch
from config import qdrant_config

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment
load_dotenv()

# Constants
COLLECTION_NAME = "ai_textbook"

def get_embedding_dimension():
    """Get the embedding dimension based on configuration."""
    use_fast_embeddings = os.getenv("USE_FAST_EMBEDDINGS", "false").lower() == "true"
    if use_fast_embeddings:
        from config import embedding_config
        return embedding_config.get_embedding_dimension()
    else:
        # Google's embedding-001 model produces 768-dimensional embeddings
        return 768

def process_and_chunk_content(text_content, all_chunks_list, file_name, chapter, section):
    """Helper function to chunk content and add it to a list with metadata."""
    chunks = text_content.split("\n\n")
    for i, chunk in enumerate(chunks):
        chunk_stripped = chunk.strip()
        if len(chunk_stripped) > 50:  # Only include chunks with substantial content
            all_chunks_list.append({
                "content": chunk_stripped,
                "metadata": {
                    "source_file": file_name,
                    "chapter": chapter,
                    "section": section,
                    "chunk_number": i
                }
            })

def load_textbook_content():
    """Load textbook content from the docs directory."""
    print("Loading textbook content...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../../.."))
    docs_dir = os.path.join(project_root, "frontend", "docusaurus-app", "docs")
    print(f"Target docs directory: {docs_dir}")
    
    doc_files_relative = ["intro.md", "chapter1.md", "chapter2.md", "chapter3.md", "chapter4.md", "chapter5.md", "chapter6.md", "chapter7.md"]
    doc_files = [os.path.join(docs_dir, f) for f in doc_files_relative]
    
    all_chunks_with_metadata = []
    
    for doc_file in doc_files:
        try:
            with open(doc_file, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"Successfully read file: {doc_file}")
        except FileNotFoundError:
            print(f"File not found: {doc_file}. Skipping.")
            continue
        
        file_name = os.path.basename(doc_file)
        chapter_title = "General Content"
        
        # Extract chapter title from the first heading
        import re
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
                    process_and_chunk_content("".join(current_section_content), all_chunks_with_metadata, file_name, chapter_title, current_section_title)
                current_section_title = section_match.group(1).strip()
                current_section_content = []
            else:
                current_section_content.append(part)
        
        # Process the last section
        if current_section_content:
            process_and_chunk_content("".join(current_section_content), all_chunks_with_metadata, file_name, chapter_title, current_section_title)
    
    print(f"Completed loading. Found {len(all_chunks_with_metadata)} total chunks.")
    return all_chunks_with_metadata

def populate_qdrant_memory():
    """Populate in-memory Qdrant with textbook content."""
    print("Populating in-memory Qdrant with textbook content...")
    
    # Initialize in-memory Qdrant client
    print("Initializing in-memory Qdrant client...")
    qdrant_client = QdrantClient(":memory:")
    
    # Create collection
    embedding_dimension = get_embedding_dimension()
    print(f"Creating collection with dimension: {embedding_dimension}")
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=embedding_dimension, distance=models.Distance.COSINE),
    )
    
    # Load textbook content
    chunks_with_metadata = load_textbook_content()
    
    if not chunks_with_metadata:
        print("No content found to populate Qdrant. Aborting.")
        return
    
    # Process in batches
    batch_size = 20
    batches = [chunks_with_metadata[i:i + batch_size] for i in range(0, len(chunks_with_metadata), batch_size)]
    print(f"Created {len(batches)} batches of size {batch_size} for processing.")
    
    total_points_upserted = 0
    
    for i, batch in enumerate(batches):
        print(f"Processing batch {i+1}/{len(batches)}...")
        contents_to_embed = [item['content'] for item in batch]
        
        try:
            # Generate embeddings for the batch
            print(f"Generating embeddings for {len(contents_to_embed)} chunks...")
            embeddings = generate_fast_embeddings_batch(contents_to_embed, "retrieval_document")
            print(f"Successfully generated {len(embeddings)} embeddings for this batch.")
            
            if len(embeddings) != len(batch):
                print(f"Mismatch: {len(batch)} chunks vs {len(embeddings)} embeddings. Skipping.")
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
            print(f"Upserted {batch_count} points for batch {i+1}.")

        except Exception as e:
            print(f"Failed to process batch {i+1}: {e}")
            import traceback
            traceback.print_exc()
    
    # Verify the data was added
    count = qdrant_client.count(collection_name=COLLECTION_NAME)
    print(f"--- Finished populating in-memory Qdrant. Total points: {count.count} ---")
    
    # Return the client so it can be used
    return qdrant_client

if __name__ == "__main__":
    populate_qdrant_memory()