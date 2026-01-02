"""
Test script to simulate a different chat request to the API
"""

import requests
import json

def test_different_chat_request():
    """Test the chat endpoint with a different sample request."""
    url = "http://localhost:8000/ask"
    
    # Create a sample chat request about a different topic
    chat_request = {
        "messages": [
            {"role": "user", "content": "What is ROS 2?"}
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
            print(f"Answer: {response_data.get('answer', '')}")
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_different_chat_request()