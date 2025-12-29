# imap/client.py 
"""
Responsibilities:
- Connect to IMAP via SSL
- Fetch exactly one unread email
- Return raw RFC822 bytes
- No parsing here
"""

import imaplib
from typing import Optional


def fetch_one_unread_email(
    username: str,
    password: str,
    host: str = "imap.gmail.com",
    port: int = 993,
) -> Optional[bytes]:
    """
    Responsibilities:
    - Connect to IMAP via SSL
    - Fetch exactly one unread email
    - Return raw RFC822 bytes
    - No parsing here
    """

    imap = imaplib.IMAP4_SSL(host, port)

    try:
        imap.login(username, password)
        imap.select("INBOX")

        status, data = imap.search(None, "UNSEEN")
        if status != "OK" or not data or not data[0]:
            return None

        # Take the first unread message only
        msg_id = data[0].split()[0]

        status, msg_data = imap.fetch(msg_id, "(RFC822)")
        if status != "OK":
            return None

        return msg_data[0][1]

    finally:
        try:
            imap.close()
        finally:
            imap.logout()
