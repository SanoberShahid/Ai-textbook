"""
Test script to verify the main API functionality works with updated Qdrant API
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import load_environment, generate_embedding
from qdrant_client import QdrantClient

def test_api_functionality():
    """Test the main API functionality."""
    print("Testing API functionality with updated Qdrant API...")
    
    # Load environment
    load_dotenv()
    
    # Initialize Qdrant client the same way as main.py
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    print(f"Qdrant client initialized with URL: {qdrant_url}")
    
    # Test embedding generation
    try:
        test_embedding = generate_embedding("Test query for RAG", "retrieval_query")
        print(f"Successfully generated embedding with {len(test_embedding)} dimensions")
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return
    
    # Test Qdrant search with the older API
    try:
        from config import qdrant_config
        collection_name = qdrant_config.QDRANT_COLLECTION_NAME

        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=test_embedding,
            limit=3,
            with_payload=True
        )

        print(f"Successfully searched Qdrant, found {len(search_results)} results")

        if search_results:
            print(f"First result content preview: {search_results[0].payload.get('content', '')[:100]}...")

    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("All API functionality tests passed!")

if __name__ == "__main__":
    test_api_functionality()