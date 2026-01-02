# Fast Embedding Configuration for AI Textbook

## Overview
This configuration enables fast local embeddings using sentence-transformers instead of API calls to Google's embedding service. This significantly improves performance and reduces costs.

## Environment Variables
The following environment variables can be set in your `.env` file:

### Embedding Configuration
- `USE_FAST_EMBEDDINGS`: Set to `true` to enable fast local embeddings, `false` to use Google API (default: `false`)
- `FAST_EMBEDDING_MODEL`: Name of the sentence-transformer model to use (default: `all-MiniLM-L6-v2`)

### Example .env Configuration
```env
USE_FAST_EMBEDDINGS=true
FAST_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Available Models
Some recommended models for fast embeddings:
- `all-MiniLM-L6-v2` - Fast and lightweight (recommended default)
- `all-MiniLM-L12-v2` - Slightly better quality, still fast
- `paraphrase-multilingual-MiniLM-L12-v2` - Good for multilingual content
- `all-mpnet-base-v2` - Higher quality but slower

## Performance Benefits
- Local execution without network latency
- No API rate limits
- Lower costs
- Better privacy (data doesn't leave your server)

## Quality Trade-offs
- Local models may have slightly lower quality than Google's embeddings
- For production use, test both options to determine which works best for your use case