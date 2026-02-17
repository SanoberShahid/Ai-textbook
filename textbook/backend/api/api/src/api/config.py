"""
Configuration module for the AI Textbook RAG API
"""

import os
from typing import Optional


class EmbeddingConfig:
    """Configuration class for embedding generation"""

    @property
    def MODEL_NAME(self) -> str:
        return os.getenv("FAST_EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    @property
    def DEVICE(self) -> Optional[str]:
        return os.getenv("EMBEDDING_DEVICE", None)

    @property
    def BATCH_SIZE(self) -> int:
        return int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))

    @property
    def NORMALIZE(self) -> bool:
        return os.getenv("NORMALIZE_EMBEDDINGS", "true").lower() == "true"

    # Supported models and their dimensions
    MODEL_DIMENSIONS = {
        "all-MiniLM-L6-v2": 384,
        "all-MiniLM-L12-v2": 384,
        "paraphrase-MiniLM-L6-v2": 384,
        "paraphrase-Multilingual-MiniLM-L12-v2": 768,
        "all-mpnet-base-v2": 768,
        "sentence-t5-xxl": 768
    }

    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension for the configured model"""
        return self.MODEL_DIMENSIONS.get(self.MODEL_NAME, 384)


embedding_config = EmbeddingConfig()
