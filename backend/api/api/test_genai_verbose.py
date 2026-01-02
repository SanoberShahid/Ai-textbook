"""
Test GenAI connection with more details
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_genai_verbose():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"API Key found: {'Yes' if api_key else 'No'}")
        genai.configure(api_key=api_key)
        try:
            # Test if the model exists
            model_info = genai.get_model('gemini-2.5-flash')
            print(f"Model info: {model_info.name}")
            print(f"Supported methods: {model_info.supported_generation_methods}")
            
            # Test generation with a simple prompt
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content('Hello, are you working?')
            print(f"GenAI is working: {str(response.text)[:200]}...")
            print(f"Response type: {type(response)}")
            print(f"Response text type: {type(response.text)}")
        except Exception as e:
            print(f'GenAI error: {e}')
            import traceback
            traceback.print_exc()
    else:
        print('No API key found')

if __name__ == "__main__":
    test_genai_verbose()