# imap/parser.py
"""
Responsibilities:
- Parse raw RFC822 email bytes into structured dictionary
- Extract fields: subject, from, to, date, body (plain text)
- Handle HTML to plain-text conversion using BeautifulSoup
- Fail fast if parsing fails
- No domain logic or classification here

Usage Context for Qwen 3 Coder:
- parse_rfc822(raw_bytes) -> dict
    Returns a dictionary with at least the following keys:
        - 'subject': str
        - 'from': str
        - 'to': str
        - 'date': str
        - 'body': str (plain text)
- Only called from main.py or pipeline orchestration
- All domain-specific decisions (classification, storage) happen outside this module
- Safe to enhance parsing (e.g., attachments, HTML fallback) but must maintain the returned dict structure
"""

from datetime import datetime
from email import message_from_bytes
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup

def parse_rfc822(raw_bytes: bytes) -> dict:
    """Parse raw RFC822 email bytes and return structured dict with plain-text body."""
    msg = message_from_bytes(raw_bytes)
    subject = msg.get("subject", "")
    from_ = msg.get("from", "")
    to = msg.get("to", "")
    date = msg.get("date", "")
    dateTime = parsedate_to_datetime(date).astimezone()

    # Extract body (prefer plain text, fallback to HTML)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body += part.get_payload(decode=True).decode(errors="ignore")
            elif content_type == "text/html" and not body:
                html = part.get_payload(decode=True).decode(errors="ignore")
                body += BeautifulSoup(html, "lxml").get_text()
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            if content_type == "text/plain":
                body = payload.decode(errors="ignore")
            elif content_type == "text/html":
                body = BeautifulSoup(payload.decode(errors="ignore"), "lxml").get_text()

    return {
        "subject": subject,
        "from": from_,
        "to": to,
        "date": dateTime.strftime("%Y-%m-%d %H:%M"), # dateTime.isoformat()
        "body": body.strip()
    }
