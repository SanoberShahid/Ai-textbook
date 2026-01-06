# Quickstart: Physical AI & Humanoid Robotics — Essentials Textbook with RAG Chatbot

This guide provides the basic steps to set up and run the project.

## Prerequisites

- Node.js v20
- Python 3.11

## Installation

### Frontend (Docusaurus)

1.  Navigate to the `frontend` directory.
2.  Install dependencies: `npm install`

### Backend (FastAPI)

1.  Navigate to the `backend` directory.
2.  Create a virtual environment: `python -m venv .venv`
3.  Activate the virtual environment.
4.  Install dependencies: `pip install -r requirements.txt`

## Running the Application

### Frontend

1.  Navigate to the `frontend` directory.
2.  Start the development server: `npm start`
3.  The Docusaurus site will be available at `http://localhost:3000`.

### Backend

1.  Navigate to the `backend` directory.
2.  Start the FastAPI server: `uvicorn main:app --reload`
3.  The API will be available at `http://localhost:8000`.

## Project Structure

The project is divided into two main parts: a `frontend` directory for the Docusaurus application and a `backend` directory for the FastAPI RAG service.
