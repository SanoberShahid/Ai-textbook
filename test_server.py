import subprocess
import time
import requests
import threading

def start_server():
    # Start the server in a subprocess
    cmd = ["python", "-c", "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"]
    process = subprocess.Popen(cmd, cwd=r"C:\Users\Pcw\Desktop\my-ai-textbook\textbook\backend\api\api")
    return process

def test_server():
    time.sleep(5)  # Wait for server to start
    try:
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Server response: {response.status_code}, {response.json()}")
        
        # Test health endpoint
        health_response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health response: {health_response.status_code}, {health_response.json()}")
        
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    print("Starting server...")
    server_process = start_server()
    
    print("Testing server...")
    test_server()
    
    # Terminate the server process
    server_process.terminate()
    server_process.wait()
    print("Server stopped.")