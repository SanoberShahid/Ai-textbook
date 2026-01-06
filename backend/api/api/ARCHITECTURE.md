[Title]: RAG-Powered AI Assistant for Docusaurus with a FastAPI Backend

This document details the architecture of a Retrieval-Augmented Generation (RAG) pipeline integrated into a Docusaurus website. It describes a workflow where the Docusaurus frontend interacts with a FastAPI backend to provide users with an AI-powered assistant that can answer questions about the site's documentation.

The implementation comprises three main components: a Docusaurus frontend for the user interface, a FastAPI server to handle backend logic and AI integration, and a Qdrant vector database for the retrieval mechanism.

The workflow involves an offline ingestion process to populate the database and an online inference process to answer user queries.

### Key Components:
- **Frontend**: A Docusaurus website (`frontend/docusaurus-app`) which contains the documentation and a custom React component for the chat interface.
- **Backend API**: A FastAPI server (`api/main.py`) that exposes endpoints for the RAG functionality, including `/ask` and `/generate_quiz`.
- **Vector Database**: A Qdrant collection (`ai_textbook`) that stores vector embeddings of the documentation content for efficient semantic search.
- **AI Models**: Google AI models, specifically `models/embedding-001` for creating vector embeddings and `gemini-pro` for generating conversational answers.

### Workflow:

#### 1. Ingestion (Offline Process)
First, the documentation content must be processed and stored in the vector database.
- The `ingest.py` script reads the markdown files from the `frontend/docusaurus-app/docs` directory.
- It chunks the content into smaller, semantically meaningful pieces.
- For each chunk, it calls the Google AI embedding model (`models/embedding-001`) to create a vector embedding.
- Finally, it upserts the original content chunk, its vector embedding, and relevant metadata (such as the source chapter and section) into the Qdrant database collection.

#### 2. Inference (Live Querying)
- A user asks a question in the chat interface on the Docusaurus site.
- The frontend sends this question to the `/ask` endpoint of the FastAPI server.
- The server generates an embedding for the question using the same embedding model.
- It then queries the Qdrant database with this embedding to retrieve the most relevant document chunks (the "Retrieval" step).
- The server constructs a detailed prompt containing the user's original question and the retrieved context from the documents.
- This prompt is sent to the `gemini-pro` generative model, which formulates an answer based on the provided context (the "Augmented Generation" step).
- The FastAPI server streams the generated answer back to the Docusaurus UI, which displays it to the user, often including citations pointing to the source documentation.

### Setup and Operation:
1.  **Prerequisites**: A Python environment, Node.js, and access credentials for Google AI and Qdrant.
2.  **Configuration**: Credentials must be configured in a `.env` file in the `api` directory.
3.  **Backend Dependencies**: Install required Python packages by running `pip install -r requirements.txt`.
4.  **Data Ingestion**: Run `python ingest.py` to populate the Qdrant database. This only needs to be done once or when the documentation changes.
5.  **Start Services**:
    -   In one terminal, run `python main.py` from the `api` directory to start the FastAPI server.
    -   In a second terminal, navigate to `frontend/docusaurus-app`, run `npm install`, and then `npm start` to launch the Docusaurus development server.
