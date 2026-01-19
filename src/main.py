import sys
import time
from imap.client import EmailClient
from llm.classify import classify_email

# Fix Windows terminal encoding for emojis/Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def process_all_emails():
    client = EmailClient()
    
    try:
        print("Connecting to mail server...")
        client.connect()
        emails = client.fetch_unread()
        
        if not emails:
            print("No new emails to process.")
            return

        print(f"Found {len(emails)} unread emails.\n")

        for msg in emails:
            print("-" * 40)
            print(f"FROM    : {msg['from']}")
            print(f"SUBJECT : {msg['subject']}")
            
            print("Calling Ollama...")
            # Classification logic
            result = classify_email(msg["body"])
            
            category = result.get("category", "Unknown")
            reason = result.get("reason", "No reason provided")

            if category == "Error":
                print(f"❌ Classification failed: {reason}")
            else:
                print(f"✅ Category: {category}")
                print(f"📝 Reason: {reason}")
                
                # Logic to move email could go here
                # client.move_to_folder(msg['uid'], category)

    except Exception as e:
        print(f"Critical error in main loop: {e}")
    finally:
        client.logout()
        print("\nLogged out safely.")

def main():
    while True:
        process_all_emails()
        print("\nWaiting 5 minutes for next check...")
        time.sleep(300)

if __name__ == "__main__":
    main()
    