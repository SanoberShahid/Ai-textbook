# RAG Chatbot Instructions

Follow these steps to run the "Ask the Book" RAG chatbot.

## 1. Setup

### a. Set Google API Key
Create a `.env` file inside the `rag_backend` directory and add your Google API key:

```
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### b. Install Python Dependencies
Navigate to the `rag_backend` directory and install the required packages using the existing virtual environment.

```bash
# Navigate to the backend directory
cd rag_backend

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
# source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

## 2. Ingest the Textbook Data

Run the `ingest.py` script from within the `rag_backend` directory. This will read the markdown files, generate embeddings, and create a `vector_db.pkl` file.

```bash
python ingest.py
```
This process may take a few moments.

## 3. Run the Backend Server

Once the ingestion is complete, start the FastAPI backend server using `uvicorn`.

```bash
uvicorn main:app --reload
```
The backend server will be running at `http://localhost:8000`.

## 4. Run the Frontend Application

In a separate terminal, navigate to the root of the `textbook` project and start the Docusaurus development server.

```bash
# Navigate to the project root
cd ..

# Start the frontend server
npm start
```
The frontend will be available at `http://localhost:3000`. You can now navigate to the "Ask the Book" page and start asking questions!
