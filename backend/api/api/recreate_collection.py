"""
Script to recreate the Qdrant collection with the correct vector dimensions for fast embeddings
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from fast_embeddings import get_fast_embedding_generator

# Load environment
load_dotenv()

def recreate_collection():
    """Recreate the Qdrant collection with correct vector dimensions."""
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ai_textbook")
    
    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    # Initialize Qdrant client
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    # Get the correct vector size from the embedding model
    generator = get_fast_embedding_generator()
    sample_embedding = generator.generate_embedding("test")
    vector_size = len(sample_embedding)
    
    print(f"Recreating collection '{collection_name}' with vector size {vector_size}...")
    
    try:
        # Delete existing collection
        client.delete_collection(collection_name=collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except Exception as e:
        print(f"Collection '{collection_name}' may not have existed: {e}")
    
    # Create new collection with correct dimensions
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE
        ),
    )
    
    print(f"Successfully created collection '{collection_name}' with vector size {vector_size}")
    
    # Verify the collection was created correctly
    collection_info = client.get_collection(collection_name)
    print(f"Collection '{collection_name}' vector size: {collection_info.config.params.vectors.size}")

if __name__ == "__main__":
    recreate_collection()