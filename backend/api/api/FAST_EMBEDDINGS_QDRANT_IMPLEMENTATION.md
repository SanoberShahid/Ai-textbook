# Fast Embeddings with Qdrant Implementation

## Overview

This implementation provides a fast, local embedding solution using sentence-transformers integrated with Qdrant vector database. This approach offers significant performance improvements over API-based embeddings while maintaining good quality.

## Key Components

### 1. FastEmbeddingGenerator (`fast_embeddings.py`)
- Uses `sentence-transformers` library with local models
- Supports various models (default: `all-MiniLM-L6-v2` which produces 384-dim vectors)
- Provides both single and batch embedding generation
- Includes similarity calculation functionality
- Configurable device usage (CPU, CUDA, etc.)

### 2. QdrantEmbeddingManager (`qdrant_embeddings.py`)
- Manages embeddings in Qdrant vector database
- Handles collection creation with correct vector dimensions
- Provides methods to add embeddings and search for similar content
- Uses optimized batch processing for efficiency

### 3. Configuration (`config.py`)
- Centralized configuration management
- Environment variable based settings
- Model, device, and performance configuration options

## Performance Improvements

- **Batch Processing**: Processing multiple texts together is significantly faster than individual processing
- **Local Embeddings**: No network latency or API rate limits
- **Optimized Vector Storage**: Qdrant provides efficient vector search capabilities

## Environment Configuration

The following environment variables can be configured in `.env`:

```env
# Qdrant Configuration
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=ai_textbook

# Fast Embeddings Configuration
USE_FAST_EMBEDDINGS=true
FAST_EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DEVICE=auto  # cpu, cuda, mps, or auto
EMBEDDING_BATCH_SIZE=32
NORMALIZE_EMBEDDINGS=true
QDRANT_DISTANCE_METRIC=Cosine
```

## Usage Examples

### Generate Single Embedding
```python
from fast_embeddings import generate_fast_embedding

embedding = generate_fast_embedding("Your text here")
print(f"Embedding has {len(embedding)} dimensions")
```

### Generate Batch Embeddings
```python
from fast_embeddings import generate_fast_embeddings_batch

texts = ["Text 1", "Text 2", "Text 3"]
embeddings = generate_fast_embeddings_batch(texts)
print(f"Generated {len(embeddings)} embeddings")
```

### Calculate Similarity
```python
from fast_embeddings import calculate_similarity

similarity = calculate_similarity("Text A", "Text B")
print(f"Similarity: {similarity}")
```

### Store and Search in Qdrant
```python
from qdrant_embeddings import add_texts_to_qdrant, search_similar_texts

# Add texts to Qdrant
texts = ["Document 1", "Document 2"]
metadata = [{"source": "doc1"}, {"source": "doc2"}]
add_texts_to_qdrant(texts, metadata)

# Search for similar content
results = search_similar_texts("Query text", top_k=5)
for result in results:
    print(f"Score: {result['score']}, Content: {result['content']}")
```

## Testing

Run the tests to verify the implementation:

```bash
# Test fast embeddings
python test_fast_embeddings.py

# Test Qdrant integration
python test_qdrant_embeddings.py
```

## Benefits

1. **Speed**: Local embeddings are much faster than API calls
2. **Cost**: No per-token costs for embeddings
3. **Privacy**: Texts don't leave your infrastructure
4. **Reliability**: No dependency on external API availability
5. **Scalability**: Can handle high throughput requirements

## Models Supported

- `all-MiniLM-L6-v2` (384 dimensions) - Default, good balance of speed and quality
- `all-MiniLM-L12-v2` (384 dimensions) - Better quality, slightly slower
- `paraphrase-Multilingual-MiniLM-L12-v2` (768 dimensions) - Multilingual support
- And many others from the sentence-transformers library