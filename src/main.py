# main.py 
"""
Responsibilities:
- Orchestrate the end-to-end flow for a single email
- Call IMAP client, parser, classifier, and storage in order
- Contain no domain logic of its own
- Act as the executable entry point
- Fail fast and log clearly
- Only orchestrate existing functions only, no new logic
"""

from imap.client import fetch_unread_email
from imap.parser import parse_rfc822
from llm.classify import classify_email
from storage.json_store import store_email_classification

def process_single_email(host, port, username, password):
    """Orchestrates the full email processing pipeline."""
    raw_email = fetch_unread_email(host, port, username, password)
    if raw_email is None:
        return

    parsed_email = parse_rfc822(raw_email)
    classification_result = classify_email(parsed_email["body"])
    result = {
        "email": parsed_email,
        "classification": classification_result
    }
    store_email_classification(result)
