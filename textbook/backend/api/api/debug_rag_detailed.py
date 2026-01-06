"""
Detailed debug script for the RAG pipeline
"""

import os
import sys
import json
from dotenv import load_dotenv
import requests

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import generate_embedding
from qdrant_client import QdrantClient
from config import qdrant_config

def debug_rag_detailed():
    """Debug the RAG pipeline with detailed logging."""
    print("=== Detailed RAG Pipeline Debug ===\n")
    
    # Load environment
    load_dotenv()
    
    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("ERROR: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collection_name = qdrant_config.QDRANT_COLLECTION_NAME
    print(f"Qdrant client initialized with URL: {qdrant_url}")
    
    # Test query
    test_query = "What is machine learning?"
    print(f"\nTesting query: '{test_query}'")
    
    # Step 1: Generate embedding
    try:
        query_embedding = generate_embedding(test_query, "retrieval_query")
        print(f"✓ Generated embedding with {len(query_embedding)} dimensions")
    except Exception as e:
        print(f"✗ Error generating embedding: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Search in Qdrant using the older API
    try:
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=3,
            with_payload=True
        )

        print(f"✓ Found {len(search_results)} results from Qdrant")

        if len(search_results) > 0:
            print("Sample search results:")
            for i, hit in enumerate(search_results):
                content = hit.payload.get('content', 'N/A')[:100]
                chapter = hit.payload.get('chapter', 'N/A')
                section = hit.payload.get('section', 'N/A')
                print(f"  {i+1}. Content: {content}...")
                print(f"     Chapter: {chapter}, Section: {section}")
        else:
            print("No results found - the collection might be empty or have no relevant content")

    except Exception as e:
        print(f"✗ Error searching Qdrant: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Format context like main.py does
    try:
        context_parts = [hit.payload.get('content', 'N/A') for hit in search_results]
        citations = [f"Source: {hit.payload.get('chapter', 'N/A')} - {hit.payload.get('section', 'N/A')}" for hit in search_results]
        context = "\n---\n".join(context_parts)
        unique_citations = "\n".join(sorted(list(set(citations))))
        
        print(f"✓ Formatted context from {len(context_parts)} results")
        print(f"  Context preview: {context[:200] if context else 'NO CONTEXT'}...")
        print(f"  Citations: {unique_citations}")
        
    except Exception as e:
        print(f"✗ Error formatting context: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Test the actual API call with detailed error info
    print(f"\nTesting API call to /ask endpoint...")
    
    url = "http://localhost:8000/ask"
    
    chat_request = {
        "messages": [
            {"role": "user", "content": test_query}
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(chat_request))
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response: {response_data}")
        else:
            print(f"Error response: {response.text}")
            
            # Let's also try to call the generate_embedding function directly to see if GenAI is working
            print(f"\nTesting GenAI directly...")
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    test_response = model.generate_content("Hello, are you working?")
                    print(f"✓ GenAI is working, test response: {str(test_response.text)[:100]}...")
                except Exception as e:
                    print(f"✗ GenAI test failed: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("✗ No GOOGLE_API_KEY found")
                
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"Error making request: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_rag_detailed()