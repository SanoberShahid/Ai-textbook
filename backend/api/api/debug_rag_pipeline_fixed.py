"""
Debug script to test the RAG pipeline step by step
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import generate_embedding
from qdrant_client import QdrantClient
from config import qdrant_config

def debug_rag_pipeline():
    """Debug the RAG pipeline step by step."""
    print("=== RAG Pipeline Debug ===\n")
    
    # Load environment
    load_dotenv()
    
    # Step 1: Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        print("ERROR: QDRANT_URL and QDRANT_API_KEY must be set in environment variables")
        return
    
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collection_name = qdrant_config.QDRANT_COLLECTION_NAME
    print(f"✓ Qdrant client initialized with URL: {qdrant_url}")
    
    # Step 2: Test embedding generation
    test_query = "What is machine learning?"
    print(f"\nStep 1: Generating embedding for query: '{test_query}'")
    
    try:
        query_embedding = generate_embedding(test_query, "retrieval_query")
        print(f"✓ Generated embedding with {len(query_embedding)} dimensions")
    except Exception as e:
        print(f"✗ Error generating embedding: {e}")
        return
    
    # Step 3: Test Qdrant search
    print(f"\nStep 2: Searching Qdrant for similar content...")
    
    try:
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=3,
            with_payload=True
        )

        print(f"✓ Found {len(search_results)} results from Qdrant")

        if len(search_results) > 0:
            print("\nSample search results:")
            for i, hit in enumerate(search_results):
                content = hit.payload.get('content', 'N/A')
                print(f"  {i+1}. Content: {content[:100]}...")
                print(f"     Payload keys: {list(hit.payload.keys())}")
        else:
            print("⚠ No results found - the collection might be empty or have no relevant content")

    except Exception as e:
        print(f"✗ Error searching Qdrant: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Test context formatting (similar to what main.py does)
    print(f"\nStep 3: Formatting context from search results...")
    
    try:
        context_parts = [hit.payload.get('content', 'N/A') for hit in search_results]
        citations = [f"Source: {hit.payload.get('chapter', 'N/A')} - {hit.payload.get('section', 'N/A')}" for hit in search_results]
        context = "\n---\n".join(context_parts)
        unique_citations = "\n".join(sorted(list(set(citations))))
        
        print(f"✓ Formatted context from {len(context_parts)} results")
        print(f"  Context preview: {context[:200] if context else 'NO CONTEXT'}")
        print(f"  Citations: {unique_citations}")
        
    except Exception as e:
        print(f"✗ Error formatting context: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Check if we have content in the right format
    print(f"\nStep 4: Validating content structure...")
    
    # Check if the docs directory exists and has content
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../.."))
    docs_dir = os.path.join(project_root, "frontend", "docusaurus-app", "docs")
    
    if os.path.exists(docs_dir):
        print(f"✓ Docs directory exists: {docs_dir}")
        doc_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
        print(f"  Found {len(doc_files)} markdown files: {doc_files}")
    else:
        print(f"⚠ Docs directory does not exist: {docs_dir}")
    
    print(f"\n=== RAG Pipeline Debug Complete ===")

if __name__ == "__main__":
    debug_rag_pipeline()