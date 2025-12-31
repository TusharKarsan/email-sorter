# imap/parser.py 
"""
Responsibilities:
- Parse RFC822 bytes
- Extract from, subject, date
- Prefer text/plain, fallback to stripped HTML
- Return normalised dict
"""

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

    def get_text_content():
        text_content = ""

        for part in msg.walk():
            content_type = part.get_content_type()
            payload = part.get_payload(decode=True)

            if not payload:
                continue

            assert isinstance(payload, bytes)

            if content_type == "text/plain":
                text_content = payload.decode("utf-8", errors="ignore")
                break

            elif content_type == "text/html":
                html_content = payload.decode("utf-8", errors="ignore")
                text_content = re.sub(r"<[^>]+>", "", html_content)

        return text_content
        

    return {
        "from": decode_header_value(msg.get("From", "")),
        "subject": decode_header_value(msg.get("Subject", "")),
        "date": parsedate_to_datetime(msg.get("Date", "")).isoformat() if msg.get("Date") else None,
        "body": get_text_content()
    }
