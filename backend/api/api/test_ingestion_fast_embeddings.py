"""
Test script to verify fast embeddings work with the ingestion process
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fast_embeddings import generate_fast_embeddings_batch
from logging_config import log

def test_ingestion_compatibility():
    """Test that fast embeddings work as expected for ingestion."""
    print("Testing ingestion compatibility with fast embeddings...")
    
    # Sample content chunks that might come from the ingestion process
    sample_chunks = [
        "Introduction to artificial intelligence and machine learning concepts.",
        "Deep learning models are a subset of machine learning that use neural networks.",
        "Natural language processing enables computers to understand human language.",
        "Computer vision allows machines to interpret and understand visual information.",
        "Reinforcement learning involves training agents to make decisions in environments."
    ]
    
    print(f"Testing with {len(sample_chunks)} sample content chunks...")
    
    try:
        # Generate embeddings for the sample chunks
        embeddings = generate_fast_embeddings_batch(sample_chunks, "retrieval_document")
        
        print(f"Successfully generated {len(embeddings)} embeddings")
        print(f"Each embedding has {len(embeddings[0])} dimensions")
        
        # Verify all embeddings were generated
        assert len(embeddings) == len(sample_chunks), "Number of embeddings doesn't match number of chunks"
        
        # Check that embeddings are reasonable (not all zeros)
        first_embedding = embeddings[0]
        assert any(val != 0.0 for val in first_embedding), "First embedding appears to be all zeros"
        
        print("[PASS] All tests passed! Fast embeddings are compatible with ingestion process.")
        return True

    except Exception as e:
        print(f"[FAIL] Error during ingestion compatibility test: {e}")
        return False


def test_embedding_dimensions():
    """Test that embeddings have the expected dimensions."""
    print("\nTesting embedding dimensions...")
    
    test_text = "Sample text for dimension testing."
    
    try:
        embedding = generate_fast_embeddings_batch([test_text])[0]
        print(f"Embedding dimension: {len(embedding)}")
        
        # all-MiniLM-L6-v2 should produce 384-dimensional embeddings
        expected_dim = 384
        if len(embedding) == expected_dim:
            print(f"[PASS] Embedding dimension {len(embedding)} matches expected {expected_dim}")
            return True
        else:
            print(f"[FAIL] Embedding dimension {len(embedding)} does not match expected {expected_dim}")
            return False

    except Exception as e:
        print(f"[FAIL] Error during dimension test: {e}")
        return False


if __name__ == "__main__":
    print("Starting ingestion compatibility tests for fast embeddings...\n")
    
    # Load environment variables
    load_dotenv()
    
    # Run tests
    test1_passed = test_ingestion_compatibility()
    test2_passed = test_embedding_dimensions()
    
    print(f"\nTest Results:")
    print(f"  Ingestion Compatibility: {'PASS' if test1_passed else 'FAIL'}")
    print(f"  Dimension Check: {'PASS' if test2_passed else 'FAIL'}")

    if test1_passed and test2_passed:
        print("\n[SUCCESS] All tests passed! Fast embeddings are ready for use with Qdrant.")
    else:
        print("\n[ERROR] Some tests failed. Please check the implementation.")