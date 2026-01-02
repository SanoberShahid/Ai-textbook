"""
Verify Qdrant client methods after API changes
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment
load_dotenv()

def verify_qdrant_methods():
    """Verify that the Qdrant client has the methods we need."""
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    # Initialize Qdrant client
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    print("Checking for required methods...")
    print(f"Has 'query_points' method: {'query_points' in dir(client)}")
    print(f"Has 'upsert' method: {'upsert' in dir(client)}")
    print(f"Has 'get_collection' method: {'get_collection' in dir(client)}")
    print(f"Has 'count' method: {'count' in dir(client)}")
    
    # Test a simple operation to make sure it works
    try:
        from config import qdrant_config
        collection_name = qdrant_config.QDRANT_COLLECTION_NAME
        count = client.count(collection_name=collection_name)
        print(f"Successfully connected to Qdrant and counted collection '{collection_name}': {count.count} items")
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")

if __name__ == "__main__":
    verify_qdrant_methods()