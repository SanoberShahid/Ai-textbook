import os
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Load environment
load_dotenv()

# Configure Google AI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and "YOUR_GOOGLE_API_KEY" not in api_key and api_key != "AIzaSyA5svuW0ETSRQWUMPE6jfbE2yU0XdXGbXI":
    genai.configure(api_key=api_key)
    print("Google GenAI Client initialized.")
else:
    print("Google API key not configured or is placeholder.")

# Create FastAPI app
app = FastAPI(title="AI Textbook RAG API", description="Minimal version for testing", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "genai_configured": bool(api_key and "YOUR_GOOGLE_API_KEY" not in api_key)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)