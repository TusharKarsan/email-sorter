# imap/parser.py 
"""
Responsibilities:
- Parse RFC822 bytes
- Extract from, subject, date
- Prefer text/plain, fallback to stripped HTML
- Return normalised dict
"""

from bs4 import BeautifulSoup
import email
import re
from email.header import decode_header
from email.utils import parsedate_to_datetime

def parse_rfc822(data):
    msg = email.message_from_bytes(data)

    def decode_header_value(value):
        if not value:
            return ""
        decoded_parts = decode_header(value)
        return ''.join(
            part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
            for part, encoding in decoded_parts
        )

    def decode_payload(part) -> str:
        payload = part.get_payload(decode=True)
        if not payload:
            return ""

        assert isinstance(payload, bytes)

        charset = part.get_content_charset() or "utf-8"

        try:
            return payload.decode(charset, errors="replace")
        except LookupError:
            # Unknown charset declared
            return payload.decode("utf-8", errors="replace")

    def get_text_content():
        text_content = ""

        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":
                text_content = decode_payload(part)
                if text_content:
                    break

            elif content_type == "text/html" and not text_content:
                html_content = decode_payload(part)
                # Parse HTML using BeautifulSoup with lxml parser
                soup = BeautifulSoup(html_content, "lxml")
                # Extract visible text with line breaks
                text_content = soup.get_text(separator="\n", strip=True)

        return text_content
        
    return {
        "from": decode_header_value(msg.get("From", "")),
        "subject": decode_header_value(msg.get("Subject", "")),
        "date": parsedate_to_datetime(msg.get("Date", "")).isoformat() if msg.get("Date") else None,
        "body": get_text_content()
    }
