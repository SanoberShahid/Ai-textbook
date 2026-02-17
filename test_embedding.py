import os
import sys
sys.path.insert(0, r'C:\Users\Pcw\Desktop\my-ai-textbook\textbook\backend\api\api')

# Set the environment variable for fast embeddings
os.environ['USE_FAST_EMBEDDINGS'] = 'true'

# Import and test the generate_embedding function from main
from main import generate_embedding

try:
    print("Testing generate_embedding function...")
    embedding = generate_embedding("This is a test", "retrieval_query")
    print(f"Success! Generated embedding with {len(embedding)} dimensions")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()