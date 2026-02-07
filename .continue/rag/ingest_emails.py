import hashlib
import os
import email
from email import policy
from bs4 import BeautifulSoup
from qdrant_client import QdrantClient
from qdrant_client.http import models
import ollama

# --- Configuration ---
DESIGN_PC_IP = "design" # Tailscale alias
QDRANT_URL = f"http://{DESIGN_PC_IP}:6333"
OLLAMA_HOST = f"http://{DESIGN_PC_IP}:11434"
COLLECTION_NAME = "email-embeddings"
EMBED_MODEL = "nomic-embed-text:latest"
EMAIL_DIR = r"D:\path\to\your\emails" # Update this path

# Initialize Clients
qdrant = QdrantClient(url=QDRANT_URL)
# Ollama client uses the OLLAMA_HOST env var if set, 
# or you can set it via client config:
os.environ["OLLAMA_HOST"] = OLLAMA_HOST

def extract_email_body(msg):
    """Extracts plain text from email body, handling HTML if necessary."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode(errors='ignore')
                break
            elif content_type == "text/html":
                html = part.get_payload(decode=True).decode(errors='ignore')
                body = BeautifulSoup(html, "html.parser").get_text()
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')
    return body.strip()

def ingest_emails():
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    
    email_files = [f for f in os.listdir(EMAIL_DIR) if f.endswith('.eml')]
    print(f"Found {len(email_files)} emails to process.")

    for idx, filename in enumerate(email_files):
        path = os.path.join(EMAIL_DIR, filename)
        
        with open(path, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=policy.default)
            
            subject = msg.get('subject', '(No Subject)')
            sender = msg.get('from', '(Unknown Sender)')
            date = msg.get('date', '')
            body = extract_email_body(msg)
            
            # 1. Generate Embedding via Ollama on Design PC
            response = ollama.embeddings(model=EMBED_MODEL, prompt=body[:2000]) # Truncate to save context
            embedding = response['embedding']
            file_hash = hashlib.md5(filename.encode()).hexdigest()
            
            # 2. Upsert into Qdrant
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    models.PointStruct(
                        id=file_hash,
                        vector=embedding,
                        payload={
                            "filename": filename,
                            "subject": subject,
                            "sender": sender,
                            "date": date,
                            "body": body[:500] # Store snippet for preview
                        }
                    )
                ]
            )
            print(f"[{idx+1}/{len(email_files)}] Indexed: {subject[:40]}...")

if __name__ == "__main__":
    if not os.path.exists(EMAIL_DIR):
        print(f"Error: {EMAIL_DIR} not found. Update the path in the script!")
    else:
        ingest_emails()
        print("\nIngestion Complete!")
