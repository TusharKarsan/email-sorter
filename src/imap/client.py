# imap/client.py
"""
Responsibilities:
- Connect to IMAP via SSL
- Fetch unread emails from folder specified in .env (default: INBOX)
- Return raw RFC822 bytes, no parsing
- Fail fast on connection or fetch errors

Usage Context for Qwen 3 Coder:
- fetch_unread_email(host, port, username, password, folder=None) -> bytes | None
- fetch_all_unread_emails(host, port, username, password, folder=None) -> list[bytes]
- folder defaults to EMAIL_FOLDER environment variable or "INBOX"
"""

import imaplib
import ssl
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
DEFAULT_FOLDER = os.environ.get("EMAIL_FOLDER", "INBOX")  # Gmail requires uppercase INBOX

SINCE_DAYS = 30  # Only fetch emails from last 45 days to limit volume

import imaplib

class EmailClient:  # <--- Verify this name matches
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.host)
        self.connection.login(self.username, self.password)
        print(f"✅ Connected to {self.host}")

    def logout(self):
        self.connection.logout()
        print(f"✅ Logged out from {self.host}")
        
    def fetch_unread_email(host, port, username, password, folder=None, since_days=SINCE_DAYS):
        """Fetch one unread email from folder, optionally only from last `since_days` days."""
        folder = folder or DEFAULT_FOLDER
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(host, port, ssl_context=context) as mail:
            mail.login(username, password)
            status, _ = mail.select(folder)
            if status != "OK":
                raise Exception(f"Failed to select folder '{folder}'. Status: {status}")

            # criteria = ["UNSEEN"]
            criteria = []
            if since_days is not None:
                since_date = (datetime.now() - timedelta(days=since_days)).strftime("%d-%b-%Y")
                criteria.append(f'SINCE {since_date}')

            status, messages = mail.search(None, *criteria)
            if status != "OK":
                raise Exception("Failed to search emails")
            email_ids = messages[0].split()
            if not email_ids:
                return None
            email_id = email_ids[0]
            status, msg = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                raise Exception(f"Failed to fetch email {email_id}")
            return msg[0][1]


    def fetch_all_unread_emails(host, port, username, password, folder=None, since_days=SINCE_DAYS):
        """Fetch all unread emails from folder, optionally only from last `since_days` days."""
        folder = folder or DEFAULT_FOLDER
        context = ssl.create_default_context()
        with imaplib.IMAP4_SSL(host, port, ssl_context=context) as mail:
            mail.login(username, password)
            status, _ = mail.select(folder)
            if status != "OK":
                raise Exception(f"Failed to select folder '{folder}'. Status: {status}")

            # criteria = ["UNSEEN"]
            criteria = []
            if since_days is not None:
                since_date = (datetime.now() - timedelta(days=since_days)).strftime("%d-%b-%Y")
                criteria.append(f'SINCE {since_date}')

            status, messages = mail.search(None, *criteria)
            if status != "OK":
                raise Exception("Failed to search emails")

            email_ids = messages[0].split()
            if not email_ids:
                return []

            raw_emails = []
            for email_id in email_ids:
                status, msg = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    raise Exception(f"Failed to fetch email {email_id}")
                raw_emails.append(msg[0][1])
            return raw_emails
