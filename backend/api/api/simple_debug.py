"""
Simple debug script to test Qdrant connection and RAG functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_client import QdrantClient
from config import qdrant_config
from fast_embeddings import generate_fast_embedding

def simple_debug():
    """Simple debug to test Qdrant connection and embeddings."""
    print("=== Simple RAG Debug ===\n")
    
    # Load environment
    load_dotenv()
    
    print(f"USE_FAST_EMBEDDINGS: {os.getenv('USE_FAST_EMBEDDINGS')}")
    print(f"QDRANT_URL: {os.getenv('QDRANT_URL')}")
    print(f"QDRANT_COLLECTION_NAME: {os.getenv('QDRANT_COLLECTION_NAME', 'ai_textbook')}")
    print()
    
    # Test embedding generation
    test_query = "What is machine learning?"
    print(f"Testing embedding generation for: '{test_query}'")
    
    try:
        embedding = generate_fast_embedding(test_query, "retrieval_query")
        print(f"[SUCCESS] Generated embedding with {len(embedding)} dimensions")
    except Exception as e:
        print(f"[ERROR] Error generating embedding: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test Qdrant connection
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("ERROR: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    try:
        print(f"Attempting to connect to Qdrant at: {qdrant_url}")
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        
        # Try to get collection info
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ai_textbook")
        try:
            collection_info = client.get_collection(collection_name)
            print(f"[SUCCESS] Successfully connected to Qdrant and found collection '{collection_name}'")
            print(f"  Collection vectors count: {collection_info.points_count}")
        except Exception as e:
            print(f"[WARNING] Collection '{collection_name}' not found: {e}")
            
        # Try a search with the embedding we generated
        try:
            search_results = client.search(
                collection_name=collection_name,
                query_vector=embedding,
                limit=3,
                with_payload=True
            )
            print(f"[SUCCESS] Search successful, found {len(search_results)} results")

            if len(search_results) > 0:
                print("\nSample search results:")
                for i, hit in enumerate(search_results):
                    content = hit.payload.get('content', 'N/A')[:100]
                    print(f"  {i+1}. Content preview: {content}...")
            else:
                print("  No results found - the collection might be empty")

        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"[ERROR] Error connecting to Qdrant: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n=== Simple RAG Debug Complete ===")

if __name__ == "__main__":
    simple_debug()