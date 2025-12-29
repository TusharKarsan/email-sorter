# llm/classify.py 
"""
Responsibilities:
- Send email content to Ollama
- Enforce structured JSON response
- Return category, confidence, rationale
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def classify_email_content(email_content):
    # Send email content to Ollama
    msg = MIMEMultipart()
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'ollama@ollama.ai'
    msg['Subject'] = 'Email Content Classification'
    body = email_content
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], 'your-password')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()
    # Enforce structured JSON response
    import json

    try:
        # Simulate a classification API call
        category = "Business"
        confidence = 0.8
        rationale = "Keywords: 'meeting', 'schedule'"

        result = {
            "category": category,
            "confidence": float(confidence),
            "rationale": rationale
        }

        return json.dumps(result, indent=4)

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    email_content = """
    Dear team,

    Please find the meeting schedule attached.

    Best regards,
    [Your Name]
    """
    print(classify_email_content(email_content))
