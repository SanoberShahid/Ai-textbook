import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:", response.status_code, response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_ask():
    """Test the ask endpoint (main chatbot functionality)"""
    try:
        payload = {
            "messages": [
                {"role": "user", "content": "Hello, can you help me understand machine learning?"}
            ]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{BASE_URL}/ask", data=json.dumps(payload), headers=headers)
        print("Chatbot Ask Endpoint:", response.status_code)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error Response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print(f"Ask test failed: {e}")
        return False

def test_explain_text():
    """Test the explain_text endpoint"""
    try:
        payload = {"text_selection": "machine learning is a subset of artificial intelligence"}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{BASE_URL}/explain_text", data=json.dumps(payload), headers=headers)
        print("Explain Text Endpoint:", response.status_code)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error Response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print(f"Explain text test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing your chatbot endpoints...")
    health_ok = test_health()
    
    if health_ok:
        print("\nTesting chatbot functionality:")
        test_ask()
        test_explain_text()
        print("\nYour chatbot should now be working! Try accessing it through your frontend or make requests to http://127.0.0.1:8000")
    else:
        print("\nHealth check failed. Please check your API keys and server logs.")
    print("Tests completed!")