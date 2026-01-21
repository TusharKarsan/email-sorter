import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

# Import our local modules using the src. prefix
from src.imap.client import EmailClient
from src.llm.classify import classify_email
from src.rules import classify_by_rule

# 1. Force UTF-8 for Windows terminal to prevent Emoji/Special Char crashes
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Load credentials from .env
load_dotenv()

def log_to_obsidian(subject, category, reason):
    """Appends classification results to a Markdown table for Obsidian."""
    log_file = "Email_Log.md"
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sanitise inputs to prevent breaking the Markdown table structure
    clean_subject = str(subject).replace("|", "-").replace("\n", " ")
    clean_reason = str(reason).replace("|", "-").replace("\n", " ")
    
    # Create file with headers if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("| Date | Subject | Category | Reason |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
    
    # Append the new row
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"| {date_str} | {clean_subject} | {category} | {clean_reason} |\n")

def process_all_emails():
    host = os.getenv("IMAP_HOST")
    user = os.getenv("IMAP_USER")
    password = os.getenv("IMAP_PASS")
    target_folder = os.getenv("EMAIL_FOLDER", "INBOX") # Default to INBOX if missing

    if not all([host, user, password]):
        print("❌ Error: Missing credentials in .env file.")
        return

    client = EmailClient(host, user, password)
    
    try:
        client.connect()
        # Pass the folder name here
        unread_messages = client.fetch_unread(folder_name=target_folder)
        
        if not unread_messages:
            print("📭 No unread emails found.")
            return

        for msg in unread_messages:
            print(f"🧐 Processing: {msg['subject']}...")
            
            try:
                # First, try to classify based on rules
                result = classify_by_rule(msg['from'], msg['subject'])
                
                # If not classified by rules, use the LLM
                if not result:
                    result = classify_email(msg["body"])

                category = result.get("category", "Unsorted")
                reason = result.get("reason", "No reason provided")
                
                print(f"✅ Categorised as: {category} ({reason})")
                
                # Update our Obsidian Log
                log_to_obsidian(msg["subject"], category, reason)
                
                # TODO: Add logic here to move email to the actual IMAP folder
                
            except Exception as e:
                print(f"⚠️ Failed to classify '{msg['subject']}': {e}")
                log_to_obsidian(msg["subject"], "Error", str(e))

    except Exception as e:
        print(f"🚨 Critical error in IMAP session: {e}")
    finally:
        client.logout()

def main():
    print("🚀 Email Sorter started (5-minute polling)...")
    while True:
        try:
            process_all_emails()
        except KeyboardInterrupt:
            print("\n👋 Script stopped by user. Exiting gracefully.")
            break
        except Exception as e:
            print(f"❗ Unexpected loop error: {e}")
        
        print("\n😴 Waiting 5 minutes for next check...")
        time.sleep(300)

if __name__ == "__main__":
    main()
    