"""
Configuration module for Qdrant embeddings setup
"""

import os
from typing import Optional


class QdrantConfig:
    """Configuration class for Qdrant embeddings"""

    @property
    def QDRANT_URL(self) -> str:
        return os.getenv("QDRANT_URL", "")

    @property
    def QDRANT_API_KEY(self) -> str:
        return os.getenv("QDRANT_API_KEY", "")

    @property
    def QDRANT_COLLECTION_NAME(self) -> str:
        return os.getenv("QDRANT_COLLECTION_NAME", "ai_textbook")

    @property
    def EMBEDDING_MODEL(self) -> str:
        return os.getenv("FAST_EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    @property
    def EMBEDDING_DEVICE(self) -> Optional[str]:
        return os.getenv("EMBEDDING_DEVICE", None)  # Auto-detect if not specified

    @property
    def EMBEDDING_DIMENSION(self) -> int:
        return 384  # Default for all-MiniLM-L6-v2

    @property
    def BATCH_SIZE(self) -> int:
        return int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))

    @property
    def NORMALIZE_EMBEDDINGS(self) -> bool:
        return os.getenv("NORMALIZE_EMBEDDINGS", "true").lower() == "true"

    @property
    def DISTANCE_METRIC(self) -> str:
        return os.getenv("QDRANT_DISTANCE_METRIC", "Cosine")

    def validate(self) -> bool:
        """Validate that required configuration values are present"""
        if not self.QDRANT_URL:
            raise ValueError("QDRANT_URL must be set in environment variables")
        if not self.QDRANT_API_KEY:
            raise ValueError("QDRANT_API_KEY must be set in environment variables")
        return True


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


# Initialize configurations
qdrant_config = QdrantConfig()
embedding_config = EmbeddingConfig()