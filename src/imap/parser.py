# imap/parser.py 
"""
Responsibilities:
- Parse RFC822 bytes
- Extract from, subject, date
- Prefer text/plain, fallback to stripped HTML
- Return normalised dict
"""

import re
from email.parser import Parser

def parse_imap_message(message_bytes):
    """
    Parse an IMAP message and return a normalised dictionary.

    :param message_bytes: bytes representing the IMAP message
    :return: dictionary containing parsed data
    """
    # Parse RFC822 bytes into Message object
    parser = Parser()
    message = parser.parsebytes(message_bytes)

    # Extract relevant fields from Message object
    result = {
        'from': re.sub(r'<[^>]*>', '', str(message['from'])),
        'subject': message.get('subject', ''),
        'date': message.get('date', '')
    }

    return result
