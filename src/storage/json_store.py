# storage/json_store.py
"""
Responsibilities:
- Persist processed email + classification result to disk
- Use JSON as the storage format
- Organise files by date (YYYY-MM-DD)
- Ensure directories exist before writing
- No business logic or classification decisions here
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

def store_email_classification(result: Dict[str, Any]) -> None:
    """Store email classification result to JSON file organized by date."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    directory = f"storage/{date_str}"
    os.makedirs(directory, exist_ok=True)

    file_path = f"{directory}/email_classification.json"

    # Read existing data if file exists
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            existing_data = json.load(f)

    # Append new result
    existing_data.append(result)

    # Write back to file
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=2)
