"""
Qdrant Embeddings Module
This module provides integration between fast embeddings and Qdrant vector database
for efficient storage and retrieval of embeddings.
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient, models
from logging_config import log
from fast_embeddings import generate_fast_embeddings_batch


class QdrantEmbeddingManager:
    """
    A class to manage embeddings in Qdrant vector database with fast embedding generation.
    """

    def __init__(self, collection_name: str = "ai_textbook", vector_size: int = None):
        """
        Initialize the Qdrant embedding manager.

        Args:
            collection_name: Name of the Qdrant collection
            vector_size: Size of the embedding vectors. If None, will be determined from the embedding model
        """
        self.collection_name = collection_name
        # Determine vector size from the embedding model if not provided
        if vector_size is None:
            from fast_embeddings import get_fast_embedding_generator
            generator = get_fast_embedding_generator()
            # Get a sample embedding to determine the size
            sample_embedding = generator.generate_embedding("test")
            self.vector_size = len(sample_embedding)
        else:
            self.vector_size = vector_size
        self.qdrant_client = self._initialize_qdrant_client()
        self._ensure_collection_exists()

    def _initialize_qdrant_client(self) -> QdrantClient:
        """Initialize Qdrant client with environment configuration."""
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if not qdrant_url or not qdrant_api_key:
            log.error("Qdrant credentials not found in .env file.")
            raise ValueError("Qdrant credentials not found in environment variables.")
        
        try:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            log.info(f"Qdrant client initialized with URL: {qdrant_url}")
            return client
        except Exception as e:
            log.error(f"Failed to initialize Qdrant client: {e}")
            raise

    def _ensure_collection_exists(self):
        """Ensure the collection exists in Qdrant with the correct vector size."""
        try:
            collections = self.qdrant_client.get_collections()
            existing_collections = [col.name for col in collections.collections]

            if self.collection_name not in existing_collections:
                log.info(f"Collection '{self.collection_name}' not found. Creating it now...")
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    ),
                )
                log.info(f"Successfully created collection '{self.collection_name}' with vector size {self.vector_size}.")
            else:
                # Check if the existing collection has the correct vector size
                collection_info = self.qdrant_client.get_collection(self.collection_name)
                existing_size = collection_info.config.params.vectors.size

                if existing_size != self.vector_size:
                    log.warning(f"Collection '{self.collection_name}' exists with vector size {existing_size}, but expected {self.vector_size}.")
                    log.warning("This may cause issues. Consider recreating the collection or using matching embeddings.")
                    # Option to recreate the collection (commented out to avoid accidental data loss)
                    # self._recreate_collection()
                else:
                    log.info(f"Collection '{self.collection_name}' already exists with correct vector size {self.vector_size}.")
        except Exception as e:
            log.error(f"Failed to check or create Qdrant collection: {e}")
            raise

    def _recreate_collection(self):
        """Recreate the collection with the correct vector size (use with caution - this will delete existing data)."""
        log.warning(f"Recreating collection '{self.collection_name}' with vector size {self.vector_size} (this will delete all existing data).")
        self.qdrant_client.delete_collection(collection_name=self.collection_name)
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE
            ),
        )
        log.info(f"Successfully recreated collection '{self.collection_name}' with vector size {self.vector_size}.")

    def add_embeddings(self, texts: List[str], metadata_list: List[Dict[str, Any]] = None, batch_size: int = 20):
        """
        Add texts with their embeddings to Qdrant.

        Args:
            texts: List of texts to embed and store
            metadata_list: Optional list of metadata dictionaries for each text
            batch_size: Number of items to process in each batch
        """
        if metadata_list is None:
            metadata_list = [{}] * len(texts)
        
        if len(texts) != len(metadata_list):
            raise ValueError("Number of texts must match number of metadata entries")
        
        # Generate embeddings in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_metadata = metadata_list[i:i + batch_size]
            
            log.info(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            
            # Generate embeddings for the batch
            embeddings = generate_fast_embeddings_batch(batch_texts, "retrieval_document")
            
            # Create Qdrant points
            points = []
            for j, (text, embedding, metadata) in enumerate(zip(batch_texts, embeddings, batch_metadata)):
                point_id = str(uuid.uuid4())
                points.append(models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={**metadata, "content": text}
                ))
            
            # Upload to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True
            )
            
            log.info(f"Upserted {len(points)} points to Qdrant collection '{self.collection_name}'")

    def search_similar(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar texts in Qdrant based on the query.

        Args:
            query_text: Text to search for similar items
            top_k: Number of similar items to return

        Returns:
            List of dictionaries containing content, metadata, and similarity scores
        """
        # Generate embedding for the query
        query_embedding = generate_fast_embeddings_batch([query_text], "retrieval_query")[0]
        
        # Search in Qdrant using the older search method for compatibility
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results
        results = []
        for hit in search_results:
            result = {
                "content": hit.payload.get("content", ""),
                "metadata": {k: v for k, v in hit.payload.items() if k != "content"},
                "score": hit.score
            }
            results.append(result)

        log.info(f"Found {len(results)} similar items for query: '{query_text[:50]}...'")
        return results

    def count_points(self) -> int:
        """
        Count the total number of points in the collection.

        Returns:
            Total number of points in the collection
        """
        try:
            count = self.qdrant_client.count(collection_name=self.collection_name)
            return count.count
        except Exception as e:
            log.error(f"Failed to count points in collection: {e}")
            return 0

    def delete_collection(self):
        """
        Delete the entire collection (use with caution!).
        """
        try:
            self.qdrant_client.delete_collection(collection_name=self.collection_name)
            log.info(f"Collection '{self.collection_name}' deleted successfully")
        except Exception as e:
            log.error(f"Failed to delete collection: {e}")
            raise


# Global instance for reuse
_qdrant_embedding_manager = None


def get_qdrant_embedding_manager() -> QdrantEmbeddingManager:
    """
    Get the global Qdrant embedding manager instance.

    Returns:
        QdrantEmbeddingManager instance
    """
    global _qdrant_embedding_manager
    if _qdrant_embedding_manager is None:
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ai_textbook")
        # Default vector size for all-MiniLM-L6-v2 model
        vector_size = 384  
        _qdrant_embedding_manager = QdrantEmbeddingManager(
            collection_name=collection_name, 
            vector_size=vector_size
        )
    return _qdrant_embedding_manager


def add_texts_to_qdrant(texts: List[str], metadata_list: List[Dict[str, Any]] = None):
    """
    Add texts with their embeddings to Qdrant.

    Args:
        texts: List of texts to embed and store
        metadata_list: Optional list of metadata dictionaries for each text
    """
    manager = get_qdrant_embedding_manager()
    manager.add_embeddings(texts, metadata_list)


def search_similar_texts(query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar texts in Qdrant based on the query.

    Args:
        query_text: Text to search for similar items
        top_k: Number of similar items to return

    Returns:
        List of dictionaries containing content, metadata, and similarity scores
    """
    manager = get_qdrant_embedding_manager()
    return manager.search_similar(query_text, top_k)


def get_embedding_count() -> int:
    """
    Count the total number of points in the collection.

    Returns:
        Total number of points in the collection
    """
    manager = get_qdrant_embedding_manager()
    return manager.count_points()