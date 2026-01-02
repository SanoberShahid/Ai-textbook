"""
Debug script to check Qdrant client methods
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment
load_dotenv()

def debug_qdrant_client():
    """Debug the Qdrant client to see available methods."""
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    # Initialize Qdrant client
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    print("Available methods in QdrantClient:")
    methods = [method for method in dir(client) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  {method}")
    
    print(f"\nHas 'search' method: {'search' in dir(client)}")
    print(f"Has 'search_points' method: {'search_points' in dir(client)}")
    
    # Try to access the search method
    if hasattr(client, 'search'):
        print("\n'search' method exists and is accessible")
    else:
        print("\n'search' method does NOT exist")

if __name__ == "__main__":
    debug_qdrant_client()