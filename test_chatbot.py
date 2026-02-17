import requests
import json

# Test the embedding functionality by calling the ask endpoint
url = "http://127.0.0.1:8000/ask"
headers = {
    'Content-Type': 'application/json'
}

payload = {
    "messages": [
        {"role": "user", "content": "What is artificial intelligence?"}
    ]
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")