"""
List available models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def list_models():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"API Key found: {'Yes' if api_key else 'No'}")
        genai.configure(api_key=api_key)
        try:
            # List all available models
            models = genai.list_models()
            print("Available models:")
            for model in models:
                print(f"  - {model.name}")
                print(f"    - Supported operations: {model.supported_generation_methods}")
        except Exception as e:
            print(f'Error listing models: {e}')
            import traceback
            traceback.print_exc()
    else:
        print('No API key found')

if __name__ == "__main__":
    list_models()