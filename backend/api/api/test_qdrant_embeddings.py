"""
Comprehensive test script for Qdrant embeddings functionality
"""

import os
import time
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_embeddings import get_qdrant_embedding_manager, search_similar_texts, get_embedding_count
from fast_embeddings import generate_fast_embedding, generate_fast_embeddings_batch, calculate_similarity
from config import qdrant_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_basic_embedding():
    """Test basic embedding generation."""
    print("Testing basic embedding generation...")
    
    test_text = "This is a test sentence for embedding."
    
    start_time = time.time()
    embedding = generate_fast_embedding(test_text)
    end_time = time.time()
    
    print(f"Generated embedding with {len(embedding)} dimensions")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"First 10 values: {embedding[:10]}")
    print("Basic embedding test completed.\n")


def test_batch_embedding():
    """Test batch embedding generation."""
    print("Testing batch embedding generation...")
    
    test_texts = [
        "This is the first test sentence.",
        "This is the second test sentence.",
        "This is the third test sentence.",
        "This is the fourth test sentence.",
        "This is the fifth test sentence."
    ]
    
    start_time = time.time()
    embeddings = generate_fast_embeddings_batch(test_texts)
    end_time = time.time()
    
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Each embedding has {len(embeddings[0])} dimensions")
    print(f"First 10 values of first embedding: {embeddings[0][:10]}")
    print("Batch embedding test completed.\n")


def test_similarity():
    """Test similarity calculation."""
    print("Testing similarity calculation...")
    
    text1 = "The cat is sitting on the mat."
    text2 = "A feline is resting on the rug."
    text3 = "The weather is sunny today."
    
    similarity_12 = calculate_similarity(text1, text2)
    similarity_13 = calculate_similarity(text1, text3)
    
    print(f"Similarity between similar sentences: {similarity_12:.4f}")
    print(f"Similarity between different sentences: {similarity_13:.4f}")
    print("Similarity test completed.\n")


def test_qdrant_integration():
    """Test Qdrant integration."""
    print("Testing Qdrant integration...")
    
    try:
        # Initialize the manager
        manager = get_qdrant_embedding_manager()
        print("Qdrant embedding manager initialized successfully")
        
        # Count existing points
        initial_count = get_embedding_count()
        print(f"Initial count of embeddings in Qdrant: {initial_count}")
        
        # Add some test data
        test_texts = [
            "Artificial intelligence is a wonderful field of study.",
            "Machine learning enables computers to learn from data.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing helps computers understand text.",
            "Computer vision allows machines to interpret visual information."
        ]
        
        test_metadata = [
            {"category": "AI", "source": "test", "id": "1"},
            {"category": "ML", "source": "test", "id": "2"},
            {"category": "Deep Learning", "source": "test", "id": "3"},
            {"category": "NLP", "source": "test", "id": "4"},
            {"category": "Computer Vision", "source": "test", "id": "5"}
        ]
        
        print("Adding test embeddings to Qdrant...")
        manager.add_embeddings(test_texts, test_metadata)
        
        # Count after adding
        after_add_count = get_embedding_count()
        print(f"Count after adding embeddings: {after_add_count}")
        
        # Search for similar content
        query = "How do computers learn from data?"
        print(f"Searching for content similar to: '{query}'")
        
        results = search_similar_texts(query, top_k=3)
        print(f"Found {len(results)} similar items:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result['score']:.4f}, Content: '{result['content'][:50]}...'")
            print(f"     Metadata: {result['metadata']}")
        
        print("Qdrant integration test completed.\n")
        
    except Exception as e:
        print(f"Error in Qdrant integration test: {e}")
        import traceback
        traceback.print_exc()
        print()


def test_performance_comparison():
    """Compare performance of single vs batch embeddings."""
    print("Testing performance comparison...")
    
    # Test single embeddings
    test_texts = [
        "This is the first test sentence.",
        "This is the second test sentence.",
        "This is the third test sentence."
    ]
    
    # Single embeddings
    start_time = time.time()
    single_embeddings = []
    for text in test_texts:
        embedding = generate_fast_embedding(text)
        single_embeddings.append(embedding)
    single_time = time.time() - start_time
    
    # Batch embeddings
    start_time = time.time()
    batch_embeddings = generate_fast_embeddings_batch(test_texts)
    batch_time = time.time() - start_time
    
    print(f"Single embeddings time: {single_time:.4f} seconds")
    print(f"Batch embeddings time: {batch_time:.4f} seconds")
    if batch_time > 0:
        print(f"Speed improvement: {single_time/batch_time:.2f}x faster")
    print("Performance comparison completed.\n")


def run_all_tests():
    """Run all tests."""
    print("Starting Qdrant embeddings tests...\n")
    
    # Load environment
    load_dotenv()
    
    # Validate configuration
    try:
        qdrant_config.validate()
        print("Configuration validation passed.\n")
    except ValueError as e:
        print(f"Configuration validation failed: {e}")
        print("Please set the required environment variables in your .env file.")
        return
    
    test_basic_embedding()
    test_batch_embedding()
    test_similarity()
    test_performance_comparison()
    test_qdrant_integration()
    
    print("All tests completed!")


if __name__ == "__main__":
    run_all_tests()