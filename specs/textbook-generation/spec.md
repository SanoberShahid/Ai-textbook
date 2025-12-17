# Specification: AI-Native Textbook with RAG Chatbot

**Feature:** textbook-generation
**Version:** 1.0

## 1. Overview

This document specifies the requirements for building an AI-native textbook platform. The platform will feature a structured, multi-chapter book on robotics and an integrated Retrieval-Augmented Generation (RAG) chatbot to answer questions about the content. The project will be built using Docusaurus for the frontend and a custom RAG backend with Qdrant, Neon, and a free-tier embeddings model.

## 2. Book Structure

The textbook will be organized into the following chapters, sourced from existing Markdown files.

1.  **Introduction to Physical AI**
2.  **Fundamentals of Humanoid Robotics**
3.  **ROS 2 Fundamentals**
4.  **Advanced ROS 2**
5.  **Real-World Robotics**
6.  **Capstone Project**

## 3. Core Features

### 3.1. Docusaurus Textbook Platform

-   **Content Rendering:** The platform will render the textbook chapters from Markdown (`.md`) files.
-   **Automated Sidebars:** The navigation sidebar will be automatically generated based on the directory structure of the book's content. This ensures maintainability as new chapters are added.
-   **Standard Docusaurus UI:** The platform will use the default Docusaurus theme and styling with minimal customizations.

### 3.2. RAG-powered Chatbot

-   **Interactive Chat Interface:** A chat component will be available on the textbook pages, allowing users to ask questions.
-   **Contextual Answers:** The chatbot will answer questions based *only* on the content of the textbook.
-   **Backend Service:** A backend service will handle the RAG pipeline, taking a user's query and returning a relevant, generated answer.

## 4. Technical Architecture

### 4.1. Frontend

-   **Framework:** Docusaurus
-   **Functionality:**
    -   Renders Markdown content.
    -   Provides navigation (sidebars, header).
    -   Integrates a chat UI component that communicates with the RAG backend.

### 4.2. Backend (RAG Service)

-   **Functionality:**
    1.  Receives a user query from the frontend.
    2.  Generates embeddings for the query using the selected embeddings model.
    3.  Queries the Qdrant vector store to find the most relevant text chunks from the textbook.
    4.  Passes the query and retrieved context to a language model to generate an answer.
    5.  Streams the answer back to the frontend.
-   **Deployment:** To be determined (e.g., Vercel Serverless Function, containerized service).

### 4.3. Data and Vector Storage

-   **Vector Database:** Qdrant (Cloud, free tier) will be used to store embeddings of the textbook content.
-   **Relational Database:** Neon (Postgres, free tier) will be used to store the original text content and metadata associated with the vectors in Qdrant. This allows for retrieving the original source text corresponding to the vectors.

### 4.4. Embeddings Model

-   **Model:** A free-tier, open-source embeddings model (e.g., from Hugging Face's MTEB leaderboard) will be used to generate vector embeddings for the textbook content and user queries. The specific model will be chosen during implementation based on performance and ease of use.

## 5. Implementation Plan & Data Flow

### 5.1. Content Pipeline (Initial Setup)

1.  **Ingestion Script:** A script will be created to:
    a. Read all `.md` files from the `docs/` directory.
    b. Chunk the text into manageable segments (e.g., paragraphs or sections).
    c. Generate embeddings for each chunk using the chosen model.
    d. Store the original text chunks and metadata in the Neon Postgres database.
    e. Store the corresponding vector embeddings in Qdrant, linking them to the text in Neon (e.g., via a unique ID).

### 5.2. Frontend Implementation

1.  **Sidebar Configuration:** Configure Docusaurus's `sidebars.ts` to automatically generate the sidebar from the `docs` directory structure.
2.  **Chat Component:** Develop or integrate a simple React chat component into the Docusaurus layout. This component will handle user input and display the streamed response from the RAG backend.

### 5.3. Backend Implementation

1.  **API Endpoint:** Create an API endpoint (e.g., `/api/chat`) that accepts a user's query.
2.  **RAG Logic:** Implement the RAG pipeline as described in section 4.2.
3.  **Database Connection:** Securely manage connection strings for Qdrant and Neon.

## 6. Phase 2 (Optional Features)

These features are not part of the initial implementation but may be considered for future versions.

-   **Urdu Translation:** Implement a workflow to translate the textbook content into Urdu. This could involve a separate Docusaurus locale.
-   **Personalized Chapters:** Explore generating personalized chapter content based on user interaction or preferences. This is a significant undertaking and would require a more advanced architecture.

## 7. Acceptance Criteria

The feature will be considered complete when:

1.  All six chapters of the textbook are rendered correctly in the Docusaurus site.
2.  The sidebar navigation is automatically generated and reflects the book structure.
3.  The chat interface is present on all textbook pages.
4.  The chatbot can answer questions accurately based on the content of the chapters.
5.  The chatbot responds with a message indicating when it cannot find a relevant answer in the text.
6.  The entire application is successfully deployed and accessible via a public URL.
7.  The content ingestion script runs successfully, populating both Neon and Qdrant.
