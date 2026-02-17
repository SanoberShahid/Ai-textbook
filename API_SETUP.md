# AI Textbook Backend Setup

## Configuration

To run the AI Textbook backend API, you need to configure the following environment variables in the `.env` file:

### Required API Keys

1. **Google API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create an account and generate an API key
   - Replace `YOUR_GOOGLE_API_KEY_HERE` in the `.env` file with your actual API key

2. **Qdrant Configuration** (Optional - defaults to in-memory mode):
   - If using cloud Qdrant: Add your Qdrant URL and API key
   - For local development: Leave empty to use in-memory storage

### Example .env file:
```
GOOGLE_API_KEY="your_actual_google_api_key_here"
QDRANT_URL=""  # Leave empty to use in-memory mode
QDRANT_API_KEY=""
USE_FAST_EMBEDDINGS="true"
```

## Features

- **Fast Embeddings**: When `USE_FAST_EMBEDDINGS="true"`, the system uses local sentence-transformer models for faster embedding generation
- **In-Memory Qdrant**: When no Qdrant credentials are provided, the system falls back to in-memory storage
- **RAG Pipeline**: Retrieval-Augmented Generation for contextual responses
- **Textbook Content Population**: Automatically loads textbook content into the vector store

## Endpoints

- `GET /health` - Check API health status
- `POST /ask` - Ask questions using RAG pipeline
- `POST /explain_text` - Get explanations for selected text
- `POST /generate_quiz` - Generate quizzes for textbook chapters

## Troubleshooting

- If endpoints return 503/500 errors, verify your Google API key is valid and has billing enabled
- Check that the Google API key has access to the Gemini models (gemini-2.5-flash)
- For Qdrant issues, ensure your credentials are correct if using cloud storage