import requests
import json

# Test the server endpoints
base_url = "http://127.0.0.1:8000"

print("Testing the AI Textbook Chatbot...")

# Test health endpoint
try:
    response = requests.get(f"{base_url}/health")
    print(f"Health: {response.status_code}, {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test explain_text endpoint
try:
    payload = {"text_selection": "What is machine learning?"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{base_url}/explain_text", data=json.dumps(payload), headers=headers)
    print(f"Explain Text: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Explain text test failed: {e}")

# Test ask endpoint
try:
    payload = {"messages": [{"role": "user", "content": "What is this textbook about?"}]}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{base_url}/ask", data=json.dumps(payload), headers=headers)
    print(f"Ask Endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Ask test failed: {e}")

print("Tests completed!")