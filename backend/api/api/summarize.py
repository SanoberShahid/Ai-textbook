import os
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

def generate_summary(content):
    """Generates a summary for the given content."""
    model = genai.GenerativeModel('gemini-pro-latest')
    prompt = f"""
    Based on the following textbook chapter, please provide a concise summary.
    The summary should capture the key concepts and main takeaways of the chapter in 2-4 paragraphs.

    Chapter Content:
    {content}

    Summary:
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    load_environment()
    chapter_files = get_chapter_files()

    for doc_file in chapter_files:
        print(f"Processing {doc_file}...")
        with open(doc_file, "r+", encoding="utf-8") as f:
            content = f.read()
            
            # Check if a summary already exists to avoid duplication
            if "## Chapter Summary" in content:
                print("  Summary already exists. Skipping.")
                continue

            summary = generate_summary(content)
            
            # Append the summary to the end of the file
            f.write("\n\n---\n\n")
            f.write("## Chapter Summary\n\n")
            f.write(summary)
            print(f"  Successfully added summary to {doc_file}")

    print("\nAll chapters have been processed.")
