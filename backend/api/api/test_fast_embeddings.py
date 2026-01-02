"""
Test script for fast embeddings functionality
"""

import os
import time
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fast_embeddings import generate_fast_embedding, generate_fast_embeddings_batch, calculate_similarity
from config import embedding_config

def test_single_embedding():
    """Test single embedding generation."""
    print("Testing single fast embedding...")

    test_text = "This is a test sentence for embedding."

    start_time = time.time()
    embedding = generate_fast_embedding(test_text)
    end_time = time.time()

    print(f"Generated embedding with {len(embedding)} dimensions")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"First 10 values: {embedding[:10]}")
    print("Single embedding test completed.\n")


def test_batch_embedding():
    """Test batch embedding generation."""
    print("Testing batch fast embedding...")

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


def test_configuration():
    """Test configuration settings."""
    print("Testing configuration settings...")

    print(f"Model: {embedding_config.MODEL_NAME}")
    print(f"Device: {embedding_config.DEVICE}")
    print(f"Batch size: {embedding_config.BATCH_SIZE}")
    print(f"Normalize: {embedding_config.NORMALIZE}")
    print(f"Embedding dimension: {embedding_config.get_embedding_dimension()}")
    print("Configuration test completed.\n")


if __name__ == "__main__":
    print("Starting fast embeddings tests...\n")

    # Load environment
    load_dotenv()

    test_configuration()
    test_single_embedding()
    test_batch_embedding()
    test_similarity()
    test_performance_comparison()

    print("All tests completed!")