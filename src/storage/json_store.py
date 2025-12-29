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

def store_email(email, classification_result):
    """
    Persist processed email and classification result to disk.

    :param email: The processed email data
    :type email: dict
    :param classification_result: The classification result
    :type classification_result: dict
    """
    # Extract date from email
    date = email['date']

    # Create directory if it doesn't exist
    dir_path = os.path.join('storage', date)
    os.makedirs(dir_path, exist_ok=True)

    # Construct file path
    file_path = os.path.join(dir_path, f'{email["id"]}.json')

    # Save JSON data to file
    with open(file_path, 'w') as f:
        json.dump(classification_result, f)

