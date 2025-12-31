# main.py
"""
Main entry point for the email sorter.

Pipeline:
1. Connect to IMAP
2. Fetch unread emails
3. Parse RFC822
4. Classify each email via Ollama (sync)
5. Store classification result
6. Print visible progress/output

See also:
- src.imap.client.fetch_all_unread_emails
- src.imap.parser.parse_rfc822
- src.llm.classify.classify_email
- src.storage.json_store.store_email_classification
"""

import os
from dotenv import load_dotenv

from src.imap.client import fetch_all_unread_emails
from src.imap.parser import parse_rfc822
from src.llm.classify import classify_email
from src.storage.json_store import store_email_classification


def process_all_emails():
    load_dotenv()

    host = os.environ.get("EMAIL_HOST")
    port = int(os.environ.get("EMAIL_PORT", 993))
    username = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    if not all([host, username, password]):
        raise RuntimeError(
            "Missing EMAIL_HOST / EMAIL_USER / EMAIL_PASS in environment"
        )

    print("Connecting to IMAP...")
    raw_emails = fetch_all_unread_emails(host, port, username, password)

    if not raw_emails:
        print("No unread emails found.")
        return

    print(f"Fetched {len(raw_emails)} unread emails")

    for idx, raw_email in enumerate(raw_emails, start=1):
        print("=" * 80)

        parsed = parse_rfc822(raw_email)

        print(f"{idx:02d}")
        print(f"FROM    : {parsed.get('from')}")
        print(f"SUBJECT : {parsed.get('subject')}")
        print(f"DATE    : {parsed.get('date')}")
        print(f"BODY LEN: {len(parsed.get('body', ''))}")
        print("Calling Ollama...")

        try:
            classification_json = classify_email(parsed["body"])
        except Exception as e:
            print("❌ Classification failed")
            print(str(e))
            classification_json = None

        record = {
            "email": parsed,
            "classification": classification_json,
        }

        store_email_classification(record)

        print("CLASSIFICATION:")
        print(classification_json)

    print("\nAll emails processed.")


def main():
    process_all_emails()


if __name__ == "__main__":
    main()
