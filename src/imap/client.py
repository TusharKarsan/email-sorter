# imap/client.py 
"""
Responsibilities:
- Connect to IMAP via SSL
- Fetch exactly one unread email
- Return raw RFC822 bytes
- No parsing here
"""

import imaplib
import ssl

def fetch_unread_email(host, port, username, password):
    """Connects to IMAP server, fetches one unread email, returns raw RFC822 bytes."""
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL(host, port, ssl_context=context) as mail:
        mail.login(username, password)
        mail.select('inbox')
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            raise Exception('Failed to search emails')
        email_ids = messages[0].split()
        if not email_ids:
            return None
        email_id = email_ids[0]
        status, msg = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            raise Exception('Failed to fetch email')
        return msg[0][1]
