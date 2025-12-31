# sanity_check_ollama.py
"""
Sanity check for Ollama / OpenAI API.
- Reads OLLAMA_BASE_URL and OLLAMA_API_KEY from .env
- Tests chat completion with llama3.1:latest
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

base_url = os.environ.get("OLLAMA_BASE_URL")
api_key = os.environ.get("OLLAMA_API_KEY")

if not base_url or not api_key:
    raise ValueError("OLLAMA_BASE_URL and OLLAMA_API_KEY must be set in .env")

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

def main():
    try:
        response = client.chat.completions.create(
            model="llama3.1:latest",
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print("Ollama response:", response.choices[0].message.content)
    except Exception as e:
        print(f"Ollama sanity check failed: {e}")

if __name__ == "__main__":
    main()
