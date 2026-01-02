import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def load_environment():
    """Loads environment variables and configures the Generative AI model."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    genai.configure(api_key=api_key)

def get_chapter_files():
    """Returns a list of all chapter markdown files."""
    return [
        "../docs/intro.md",
        "../docs/chapter1.md",
        "../docs/chapter2.md",
        "../docs/chapter3.md",
        "../docs/chapter4.md",
        "../docs/chapter5.md",
        "../docs/chapter6.md",
        "../docs/chapter7.md",
    ]

def generate_quiz(content):
    """Generates 3-5 multiple-choice questions for the given content."""
    model = genai.GenerativeModel('gemini-pro-latest')
    prompt = f"""
    Based on the following textbook chapter, generate 3-5 multiple-choice questions.
    Each question should have 4 options, and you must clearly indicate the correct answer.
    Format the output as a JSON array of objects, where each object has:
    - "question": The question text.
    - "options": An array of 4 strings for the answer options.
    - "correctAnswer": The correct answer string (must match one of the options).

    Chapter Content:
    {content}

    Example JSON structure for one question:
    {{
      "question": "What is the capital of France?",
      "options": ["London", "Paris", "Berlin", "Rome"],
      "correctAnswer": "Paris"
    }}

    Quiz Questions (JSON array):
    """
    response = model.generate_content(prompt)
    
    # Attempt to parse the JSON response
    try:
        quiz_data = json.loads(response.text)
        # Basic validation
        if not isinstance(quiz_data, list) or not all(isinstance(q, dict) and 'question' in q and 'options' in q and 'correctAnswer' in q for q in quiz_data):
            raise ValueError("Invalid JSON structure returned by the model.")
        return quiz_data
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {response.text}")
        return None
    except ValueError as e:
        print(f"Validation error for quiz data: {e}, Response: {response.text}")
        return None

if __name__ == "__main__":
    load_environment()
    chapter_files = get_chapter_files()

    for doc_file in chapter_files:
        print(f"Processing {doc_file}...")
        with open(doc_file, "r+", encoding="utf-8") as f:
            content = f.read()
            
            # Check if quiz already exists
            if "<Quiz data={" in content:
                print("  Quiz already exists. Skipping.")
                continue

            quiz_data = generate_quiz(content)
            
            if quiz_data:
                # Append the quiz to the end of the file
                f.write("\n\n---\n\n")
                f.write("## Quiz\n\n")
                f.write("```jsx\n")
                f.write("<Quiz data={")
                f.write(json.dumps(quiz_data, indent=2))
                f.write(" />\n")
                f.write("```\n")
                print(f"  Successfully added quiz to {doc_file}")
            else:
                print(f"  Failed to generate quiz for {doc_file}. Skipping.")

    print("\nAll chapters have been processed for quizzes.")
