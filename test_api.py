import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:", response.status_code, response.json())
    except Exception as e:
        print(f"Health check failed: {e}")

def test_explain_text():
    """Test the explain_text endpoint"""
    try:
        payload = {"text_selection": "Machine learning is a subset of artificial intelligence"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{BASE_URL}/explain_text", data=json.dumps(payload), headers=headers)
        print("Explain Text:", response.status_code, response.json() if response.status_code == 200 else response.text)
    except Exception as e:
        print(f"Explain text test failed: {e}")

def test_ask():
    """Test the ask endpoint"""
    try:
        payload = {
            "messages": [
                {"role": "user", "content": "What is machine learning?"}
            ]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{BASE_URL}/ask", data=json.dumps(payload), headers=headers)
        print("Ask Endpoint:", response.status_code, response.json() if response.status_code == 200 else response.text)
    except Exception as e:
        print(f"Ask test failed: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_health()
    test_explain_text()
    test_ask()
    print("Tests completed!")