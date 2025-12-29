# llm/classify.py 
"""
Responsibilities:
- Send email content to Ollama
- Enforce structured JSON response
- Return category, confidence, rationale
- Call get_classification_prompt() defined in @file prompts.py and return JSON string
- No prompt construction here
"""

import json
import subprocess
import sys

def classify_email(email_content: str) -> str:
    try:
        # Get the prompt from prompts.py
        from prompts import get_classification_prompt
        prompt = get_classification_prompt(email_content)

        # Prepare the Ollama command
        cmd = [
            "ollama", "run", "llama3",
            prompt
        ]

        # Run the command and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception(f"Ollama error: {result.stderr}")

        # Parse the JSON response
        response = result.stdout.strip()
        parsed = json.loads(response)

        # Return the structured response
        return json.dumps(parsed, indent=2)

    except Exception as e:
        # Re-raise any exception as a generic error
        raise Exception(f"Classification failed: {str(e)}")
