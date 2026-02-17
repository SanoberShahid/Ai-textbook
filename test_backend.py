import requests
import json

# Test the backend API directly
url = "http://127.0.0.1:8000/ask"

# Sample request that mimics what the frontend would send
sample_request = {
    "messages": [
        {
            "role": "user",
            "content": "What is artificial intelligence?"
        }
    ]
}

print("Testing the backend API...")
print(f"Sending request to: {url}")
print(f"Request data: {json.dumps(sample_request, indent=2)}")

try:
    response = requests.post(url, json=sample_request, timeout=30)
    print(f"\nResponse status code: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"Response body: {response.json()}")
    else:
        print(f"Response body: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the backend. Make sure the server is running on http://127.0.0.1:8000")
except requests.exceptions.Timeout:
    print("Error: Request timed out. The API might be taking too long to respond.")
except Exception as e:
    print(f"Error: {str(e)}")