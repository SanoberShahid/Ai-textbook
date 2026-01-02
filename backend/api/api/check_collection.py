"""
Check what's in the Qdrant collection
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from config import qdrant_config

def check_collection():
    """Check what's in the Qdrant collection."""
    load_dotenv()
    
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collection_name = qdrant_config.QDRANT_COLLECTION_NAME
    
    # Count items
    count = client.count(collection_name=collection_name)
    print(f"Total items in collection: {count.count}")
    
    # Get a few sample items
    if count.count > 0:
        scroll_result = client.scroll(
            collection_name=collection_name,
            limit=5,  # Get first 5 items
            with_payload=True,
            with_vectors=False
        )
        
        points, _ = scroll_result
        print(f"\nSample items in collection:")
        for i, point in enumerate(points):
            content = point.payload.get('content', 'N/A')[:100]  # First 100 chars
            print(f"  {i+1}. Content preview: {content}...")
            print(f"     Metadata: {point.payload.get('chapter', 'N/A')}, {point.payload.get('section', 'N/A')}")
    else:
        print("Collection is empty. You may need to run the ingestion script.")

if __name__ == "__main__":
    check_collection()