"""
Test script to verify in-memory Qdrant functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_client import QdrantClient, models
from fast_embeddings import generate_fast_embedding

# Load environment
load_dotenv()

def test_in_memory_qdrant():
    """Test in-memory Qdrant functionality."""
    print("Testing in-memory Qdrant...")
    
    # Initialize in-memory Qdrant client
    client = QdrantClient(":memory:")
    
    # Create a collection
    collection_name = "test_collection"
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),  # Size for all-MiniLM-L6-v2
    )
    print("Created in-memory collection")
    
    # Add some test data
    test_texts = [
        "Artificial intelligence is a wonderful field of study.",
        "Machine learning enables computers to learn from data.",
        "Deep learning uses neural networks with multiple layers."
    ]
    
    import uuid
    points = []
    for i, text in enumerate(test_texts):
        embedding = generate_fast_embedding(text, "retrieval_document")
        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"content": text, "id": i}
        )
        points.append(point)
    
    # Upload to Qdrant
    client.upsert(collection_name=collection_name, points=points)
    print(f"Upserted {len(points)} points")
    
    # Verify count
    count = client.count(collection_name=collection_name)
    print(f"Collection contains {count.count} points")
    
    # Search for similar content
    query_text = "How do computers learn?"
    query_embedding = generate_fast_embedding(query_text, "retrieval_query")

    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=2,
        with_payload=True
    )

    print(f"Found {len(search_results)} similar items:")
    for i, hit in enumerate(search_results):
        print(f"  {i+1}. Score: {hit.score:.4f}, Content: '{hit.payload['content'][:50]}...'")

    print("In-memory Qdrant test completed successfully!")

if __name__ == "__main__":
    test_in_memory_qdrant()