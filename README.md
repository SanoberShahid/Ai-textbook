<<<<<<< HEAD
# Physical AI & Humanoid Robotics Textbook

This repository contains the source code for the "Physical AI & Humanoid Robotics" textbook, built using Docusaurus, alongside a Python API for interactive features. The goal of this project is to provide a comprehensive and interactive learning experience on Physical AI and Humanoid Robotics, adhering to the principles of simplicity, accuracy, and minimalism.

## Project Structure

This project is organized into two main components:

*   **`frontend/docusaurus-app/`**: Contains the Docusaurus-based textbook website, including documentation, blog, and UI components.
*   **`backend/api/api/`**: Contains the Python-based API for serverless functions and backend logic (e.g., quiz generation, RAG chatbot).

## Getting Started

### Prerequisites

*   Node.js (LTS version)
*   Yarn (for frontend)
*   Python 3.x (for backend)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/user/repo.git
    ```
2.  Navigate to the repository root:
    ```bash
    cd textbook
    ```
3.  **Frontend Setup**:
    ```bash
    cd frontend/docusaurus-app
    yarn install
    cd ../..
    ```
4.  **Backend Setup**:
    ```bash
    cd backend/api/api
    pip install -r requirements.txt # Or create a virtual environment first: python -m venv .venv && ./.venv/bin/activate (or .\.venv\Scripts\activate for Windows) && pip install -r requirements.txt
    cd ../../..
    ```

### Local Development

#### Frontend (Docusaurus Textbook)

To start the local development server for the textbook:

```bash
cd frontend/docusaurus-app
yarn start
```

This command starts a local development server and opens a browser window at `http://localhost:3000`. Most changes are reflected live without having to restart the server.

#### Backend (Python API)

To run the local backend API:

```bash
cd backend/api/api
python main.py # Or your specific entry point
```

(Ensure your Python virtual environment is activated if you created one.)

### Build

To build the static content for the Docusaurus textbook:

```bash
cd frontend/docusaurus-app
yarn build
```

This command generates static content into the `build` directory within `frontend/docusaurus-app/`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
=======
# My AI Textbook

This is the repository for my AI textbook project.
>>>>>>> a669881 (Initial commit from Specify template)
