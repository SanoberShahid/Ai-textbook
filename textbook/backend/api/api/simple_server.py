import threading
import time
from main import app
import uvicorn

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    # Run server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Server started in background thread")
    print("Waiting for server to initialize...")
    
    # Wait for a bit to allow server to start
    time.sleep(5)
    
    print("Server should be running now")
    
    # Keep main thread alive
    try:
        while server_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")