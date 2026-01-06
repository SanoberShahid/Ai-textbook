# Health Checks

This document describes the health check endpoints for the services in this project.

## Backend API (`/api`)

The FastAPI application provides a health check endpoint to verify its status.

*   **Endpoint:** `/health`
*   **Method:** `GET`
*   **Success Response:**
    *   **Code:** 200 OK
    *   **Content:** `{"status": "ok"}`
