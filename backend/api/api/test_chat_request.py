"""
Test script to simulate a chat request to the API
"""

import requests
import json
from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

def test_chat_request():
    """Test the chat endpoint with a sample request."""
    url = "http://localhost:8000/ask"
    
    # Create a sample chat request
    chat_request = {
        "messages": [
            {"role": "user", "content": "What is machine learning?"}
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Sending chat request to the API...")
        response = requests.post(url, headers=headers, data=json.dumps(chat_request))
        
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response: {response_data}")
            print("\nAnswer received successfully!")
            print(f"Answer preview: {response_data.get('answer', '')[:200]}...")
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_chat_request()