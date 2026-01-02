"""
Fast Embeddings Module
This module provides local embedding generation using sentence-transformers
for faster performance compared to API-based embeddings.
"""

import os
from typing import List, Union
from sentence_transformers import SentenceTransformer
from logging_config import log
import numpy as np


class FastEmbeddingGenerator:
    """
    A class to generate fast embeddings using local sentence-transformer models.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = None):
        """
        Initialize the embedding generator with a pre-trained model.

        Args:
            model_name: Name of the sentence-transformer model to use
            device: Device to run the model on (e.g., 'cpu', 'cuda', 'mps').
                   If None, will auto-detect (GPU if available)
        """
        self.model_name = model_name
        self.device = device
        self._model = None
        self._load_model()

    def _load_model(self):
        """Load the sentence-transformer model."""
        try:
            log.info(f"Loading sentence-transformer model: {self.model_name} on device: {self.device or 'auto'}")
            self._model = SentenceTransformer(self.model_name, device=self.device)
            log.info(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            log.error(f"Failed to load sentence-transformer model {self.model_name}: {e}")
            raise

    @property
    def model(self):
        """Get the loaded model, loading it if necessary."""
        if self._model is None:
            self._load_model()
        return self._model

    def generate_embedding(self, text: str, task_type: str = "retrieval_document", normalize: bool = True) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed
            task_type: Type of task (for compatibility with existing API)
            normalize: Whether to normalize the embedding vector

        Returns:
            List of embedding values
        """
        try:
            embedding = self.model.encode([text], normalize_embeddings=normalize)[0].tolist()
            log.info(f"Generated embedding for task type: {task_type}, text length: {len(text)}")
            return embedding
        except Exception as e:
            log.error(f"Failed to generate embedding: {e}")
            raise

    def generate_embeddings_batch(self, texts: List[str], task_type: str = "retrieval_document", normalize: bool = True, batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts with optimized processing.

        Args:
            texts: List of input texts to embed
            task_type: Type of task (for compatibility with existing API)
            normalize: Whether to normalize the embedding vectors
            batch_size: Size of internal batches for processing large lists

        Returns:
            List of embedding lists
        """
        try:
            # Process in chunks to handle large lists efficiently
            all_embeddings = []
            for i in range(0, len(texts), batch_size):
                chunk = texts[i:i + batch_size]
                chunk_embeddings = self.model.encode(chunk, normalize_embeddings=normalize).tolist()
                all_embeddings.extend(chunk_embeddings)

            log.info(f"Generated embeddings for {len(texts)} texts, task type: {task_type}")
            return all_embeddings
        except Exception as e:
            log.error(f"Failed to generate embeddings batch: {e}")
            raise

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity score between 0 and 1
        """
        try:
            embeddings = self.model.encode([text1, text2], normalize_embeddings=True)
            similarity = float(np.dot(embeddings[0], embeddings[1]))
            return similarity
        except Exception as e:
            log.error(f"Failed to calculate similarity: {e}")
            raise


# Global instance for reuse
_fast_embedding_generator = None


def get_fast_embedding_generator() -> FastEmbeddingGenerator:
    """
    Get the global fast embedding generator instance.

    Returns:
        FastEmbeddingGenerator instance
    """
    global _fast_embedding_generator
    if _fast_embedding_generator is None:
        model_name = os.getenv("FAST_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        device = os.getenv("EMBEDDING_DEVICE", None)  # Allow specifying device via env var
        _fast_embedding_generator = FastEmbeddingGenerator(model_name=model_name, device=device)
    return _fast_embedding_generator


def generate_fast_embedding(text: str, task_type: str = "retrieval_document", normalize: bool = True) -> List[float]:
    """
    Generate a single fast embedding.

    Args:
        text: Input text to embed
        task_type: Type of task (for compatibility with existing API)
        normalize: Whether to normalize the embedding vector

    Returns:
        List of embedding values
    """
    generator = get_fast_embedding_generator()
    return generator.generate_embedding(text, task_type, normalize)


def generate_fast_embeddings_batch(texts: List[str], task_type: str = "retrieval_document", normalize: bool = True, batch_size: int = 32) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts.

    Args:
        texts: List of input texts to embed
        task_type: Type of task (for compatibility with existing API)
        normalize: Whether to normalize the embedding vectors
        batch_size: Size of internal batches for processing large lists

    Returns:
        List of embedding lists
    """
    generator = get_fast_embedding_generator()
    return generator.generate_embeddings_batch(texts, task_type, normalize, batch_size)


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Cosine similarity score between 0 and 1
    """
    generator = get_fast_embedding_generator()
    return generator.similarity(text1, text2)