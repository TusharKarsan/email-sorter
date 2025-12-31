# llm/classify.py
"""
Responsibilities:
- Send email content to remote Ollama server (Llama 3.1) for classification
- Enforce structured JSON response with keys: category (str), confidence (float 0-1), rationale (str)
- Validate JSON keys and types; raise ValueError if missing or incorrect
- Provide both sync (classify_email) and async batch (classify_emails_batch_async) functions
- No prompt construction; use get_classification_prompt from prompts.py
- Fail fast on network or parsing errors

Usage Context for Qwen 3 Coder:
- classify_email(email_body: str) -> str
    - Returns JSON string with keys: category, confidence, rationale
    - Called from main.py for single email processing
- classify_emails_batch_async(email_contents: list[str]) -> list[str]
    - Returns list of JSON strings for batch classification
    - Called from main.py or async orchestration
- get_classification_prompt(email_text: str) -> str
    - Defined in prompts.py, returns the deterministic prompt string for LLM
- Do not modify the structure of the returned JSON
- Safe to handle exceptions, retries, or network errors internally
"""

import asyncio, json, os
from openai import OpenAI
from typing import List

base_url = os.environ.get("OLLAMA_BASE_URL")
api_key = os.environ.get("OLLAMA_API_KEY")

def classify_email(email_content: str) -> str:
    """Sync classification of a single email using remote Ollama Llama 3.1."""
    from src.llm.prompts import get_classification_prompt

    client = OpenAI(base_url=base_url, api_key=api_key)
    prompt = get_classification_prompt(email_content)

    response = client.chat.completions.create(
        model="llama3.1:latest",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content.strip()
    parsed = json.loads(reply)

    # Validate keys
    required_keys = {"category": str, "confidence": (float, int), "rationale": str}
    for key, expected_type in required_keys.items():
        if key not in parsed:
            raise ValueError(f"Missing key '{key}' in response")
        if not isinstance(parsed[key], expected_type):
            raise ValueError(f"Key '{key}' has wrong type. Expected {expected_type}, got {type(parsed[key])}")

    if not 0 <= parsed["confidence"] <= 1:
        raise ValueError(f"Confidence out of range: {parsed['confidence']}")

    return json.dumps(parsed, indent=2)


async def _classify_single(client: OpenAI, email_text: str) -> str:
    """Internal async helper to classify a single email."""
    from src.llm.prompts import get_classification_prompt

    prompt = get_classification_prompt(email_text)
    response = await client.chat.completions.acreate(
        model="llama3.1:latest",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content.strip()
    parsed = json.loads(reply)

    # Validate keys
    required_keys = {"category": str, "confidence": (float, int), "rationale": str}
    for key, expected_type in required_keys.items():
        if key not in parsed:
            raise ValueError(f"Missing key '{key}' in response")
        if not isinstance(parsed[key], expected_type):
            raise ValueError(f"Key '{key}' has wrong type. Expected {expected_type}, got {type(parsed[key])}")

    if not 0 <= parsed["confidence"] <= 1:
        raise ValueError(f"Confidence out of range: {parsed['confidence']}")

    return json.dumps(parsed, indent=2)


async def classify_emails_batch_async(email_contents: List[str]) -> List[str]:
    """Async batch classification of multiple emails."""
    client = OpenAI(base_url=base_url, api_key=api_key)
    tasks = [_classify_single(client, email) for email in email_contents]
    return await asyncio.gather(*tasks)
