# sanity_check_gmail.py
"""
Sanity check for Gmail IMAP access using app-password.
- Reads host, port, username, password, and folder from .env
- Verifies login, folder selection, and email search
"""

import os
import ssl
import imaplib
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("EMAIL_HOST")
port = int(os.environ.get("EMAIL_PORT", 993))
username = os.environ.get("EMAIL_USER")
password = os.environ.get("EMAIL_PASS")
folder = os.environ.get("EMAIL_FOLDER", "INBOX")  # Gmail requires uppercase INBOX

def main():
    context = ssl.create_default_context()
    try:
        with imaplib.IMAP4_SSL(host, port, ssl_context=context) as mail:
            mail.login(username, password)
            status, _ = mail.select(folder)
            if status != "OK":
                raise Exception(f"Failed to select folder '{folder}'. Status: {status}")
            status, messages = mail.search(None, "ALL")
            if status != "OK":
                raise Exception("Failed to search emails")
            print(f"Successfully connected. {len(messages[0].split())} emails in folder '{folder}'.")
    except Exception as e:
        print(f"IMAP sanity check failed: {e}")

if __name__ == "__main__":
    main()
