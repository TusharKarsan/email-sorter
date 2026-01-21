from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytest
from src.imap.parser import parse_rfc822

def test_parse_simple_plain_text_email():
    raw_email = b"From: sender@example.com\nTo: receiver@example.com\nSubject: Test Subject\n\nThis is the body."
    parsed = parse_rfc822(raw_email)
    assert parsed["subject"] == "Test Subject"
    assert parsed["from"] == "sender@example.com"
    assert parsed["to"] == "receiver@example.com"
    assert parsed["body"] == "This is the body."

def test_parse_multipart_email_with_plain_text():
    msg = MIMEMultipart()
    msg["Subject"] = "Multipart Test"
    msg["From"] = "multipart@example.com"
    msg["To"] = "receiver@example.com"
    msg.attach(MIMEText("This is the plain text part.", "plain"))
    raw_email = msg.as_bytes()

    parsed = parse_rfc822(raw_email)
    assert parsed["subject"] == "Multipart Test"
    assert parsed["body"] == "This is the plain text part."

def test_parse_multipart_email_with_html():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "HTML Test"
    msg["From"] = "html@example.com"
    msg["To"] = "receiver@example.com"
    msg.attach(MIMEText("This is plain.", "plain"))
    msg.attach(MIMEText("<html><body><p>This is HTML.</p></body></html>", "html"))
    raw_email = msg.as_bytes()
    
    parsed = parse_rfc822(raw_email)
    assert parsed["subject"] == "HTML Test"
    # The parser prefers plain text, so it should find that first
    assert parsed["body"] == "This is plain."

def test_parse_simple_html_email():
    raw_email = b"From: htmlsender@example.com\nTo: receiver@example.com\nSubject: HTML Subject\nContent-Type: text/html\n\n<html><body><h1>Hello</h1><p>This is a paragraph.</p></body></html>"
    parsed = parse_rfc822(raw_email)
    assert parsed["subject"] == "HTML Subject"
    assert parsed["body"] == "Hello\nThis is a paragraph."

def test_parse_email_with_no_body():
    raw_email = b"From: nobody@example.com\nTo: receiver@example.com\nSubject: No Body Test\n\n"
    parsed = parse_rfc822(raw_email)
    assert parsed["body"] == ""

def test_parse_email_with_date():
    raw_email = b"Date: Mon, 20 Jan 2026 10:00:00 -0500\nFrom: sender@example.com\nTo: receiver@example.com\nSubject: Date Test\n\nBody"
    parsed = parse_rfc822(raw_email)
    # The date is converted to local timezone. The exact value depends on the test runner's timezone.
    # We can check the format.
    assert "2026-01-20" in parsed["date"]

def test_parse_only_html_in_multipart():
    # Test case where only HTML is present in a multipart email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Only HTML'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'
    
    html_part = MIMEText('<html><body><p>This is the HTML body.</p></body></html>', 'html')
    msg.attach(html_part)
    
    parsed = parse_rfc822(msg.as_bytes())
    
    assert parsed['body'] == 'This is the HTML body.'
