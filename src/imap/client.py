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
import email
from email.header import decode_header

class EmailClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.mail = None

    def connect(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.host)
            self.mail.login(self.username, self.password)
            print(f"✅ Connected to {self.host}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise

    def fetch_unread(self):
        """Searches for UNSEEN emails and returns a list of message objects."""
        self.mail.select("inbox")
        # Search for all unread emails
        status, response = self.mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            print("❌ Failed to search for emails.")
            return []

        messages = []
        # response[0] contains space-separated IDs
        for num in response[0].split():
            # Fetch the email body (RFC822)
            status, data = self.mail.fetch(num, '(RFC822)')
            if status != 'OK':
                continue
            
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Store ID and message object
            messages.append({
                "id": num,
                "subject": msg["Subject"],
                "from": msg["From"],
                "body": self._get_body(msg)
            })
        return messages

    def _get_body(self, msg):
        """Helper to extract plain text body from email."""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            return msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return ""

    def logout(self):
        if self.mail:
            self.mail.logout()
            print(f"✅ Logged out from {self.host}")
