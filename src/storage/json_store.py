# storage/json_store.py
"""
Responsibilities:
- Persist parsed emails and classification results to local storage
- Store data in JSON format
- Fail fast if writing fails
- No domain logic, parsing, or classification here
- Ensure consistent structure for downstream analysis or review

Usage Context for Qwen 3 Coder:
- store_email_classification(data: dict) -> None
    - `data` dictionary will contain at least:
        - 'email': dict (output from imap/parser.py)
        - 'classification': str or JSON string (output from llm/classify.py)
    - Called from main.py after processing each email
    - Should append to a JSON file or maintain cumulative storage
- Do not modify the structure of the stored dict
- Safe to implement file locking or error handling for concurrent writes
"""

import json
import os

STORE_FILE = "emails_classified.json"

def store_email_classification(data: dict) -> None:
    """Append a single email classification result to the JSON store."""
    # Ensure file exists
    if not os.path.exists(STORE_FILE):
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    # Read existing data
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    # Append new entry
    existing_data.append(data)

    # Write back
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)
