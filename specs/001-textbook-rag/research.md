# Research: Physical AI & Humanoid Robotics — Essentials Textbook with RAG Chatbot

This document captures the research and decisions made to resolve the "NEEDS CLARIFICATION" items in the implementation plan.

## Research Tasks

### 1. Language and Framework Versions

**Task**: Determine the optimal and most stable versions for Python/FastAPI and Node.js/Docusaurus.
**Findings**:
- **Python**: 3.11 is a stable and widely used version. We will use **Python 3.11**.
- **Node.js**: v20 is the current LTS version. We will use **Node.js v20**.
- **FastAPI**: The latest version is recommended for new projects. We will use the **latest stable version of FastAPI**.
- **Docusaurus**: The latest version is recommended. We will use the **latest stable version of Docusaurus**.

### 2. Testing Frameworks

**Task**: Select appropriate testing frameworks for the Python backend and the React frontend.
**Findings**:
- **Python/FastAPI**: `pytest` is the de-facto standard for testing in the Python community, with rich plugin support for FastAPI. We will use **pytest**.
- **React/Docusaurus**: `Jest` is a popular choice for testing React applications, and is often used with `React Testing Library`. We will use **Jest**.

### 3. Scale and Scope

**Task**: Define the expected scale for the textbook to inform the chunking strategy and database capacity planning.
**Findings**:
- **Initial Scale**: The textbook will have 6 chapters. Assuming each chapter is a long-form document, we can estimate the initial content to be around 50-100 pages.
- **User Load**: As a free-tier project, the expected user load is low to moderate. The architecture should be able to handle a few concurrent users.
- **Chunking Strategy**: Given the moderate scale, a simple chunking strategy based on paragraphs or sections should be sufficient. We will use a chunk size of 512 tokens with an overlap of 64 tokens. This is a common practice and should work well with free-tier embedding models.

### 4. Best Practices and Integration Patterns

**Task**: Research best practices for integrating the selected technologies.
**Findings**:
- **Docusaurus and RAG**: The RAG chatbot will be integrated as a React component within the Docusaurus site. The component will make API calls to the FastAPI backend.
- **FastAPI and RAG**: The FastAPI backend will handle the RAG logic, including querying the Qdrant vector store and generating answers. It will expose a simple API endpoint for the frontend to consume.
- **Qdrant and Neon**: Qdrant will be used for vector similarity search. Neon (PostgreSQL) can be used to store metadata about the documents, but for the initial implementation, we might not need it. We will start with just Qdrant and introduce Neon if needed. This aligns with the "Simplicity" and "Minimalism" principles.
