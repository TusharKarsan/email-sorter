# src/scripts/sanity_check_samples.py
import os
from pathlib import Path
from src.imap.parser import parse_rfc822

# Map keywords in filenames to categories
CATEGORY_KEYWORDS = {
    "application_received": ["Application Received", "Application Recieved", "Application  Received", "Application Sent"],
    "application_rejected": ["Application Rejected"],
    "job_opening": ["Opening - New job openings"],
    "irrelevant": ["Not Relevant", "Irrelevant"]
}

def classify_email(filename: str) -> str:
    """Return category based on keywords in filename"""
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in filename for k in keywords):
            return category
    return "unknown"

def preview_text(text: str, length: int = 120) -> str:
    """Return first `length` characters of text for preview"""
    text = text.replace("\n", " ").strip()
    return (text[:length] + "...") if len(text) > length else text

def main():
    emails_dir = Path("data/samples/eml")
    eml_files = sorted(emails_dir.glob("*.eml"))

    for idx, eml_file in enumerate(eml_files, start=1):
        with open(eml_file, "rb") as f:
            data = f.read()

        parsed = parse_rfc822(data)
        category = classify_email(eml_file.name)
        body_preview = preview_text(parsed["body"], 120)

        print("="*80)
        print(f"{idx:02d} {eml_file.name}")
        print(f"FROM   : {parsed['from']}")
        print(f"SUBJ   : {parsed['subject']}")
        print(f"DATE   : {parsed['date']}")
        print(f"LEN    : {len(parsed['body'])}")
        print(f"CATEGORY: {category}")
        print(f"PREVIEW: {body_preview}")

if __name__ == "__main__":
    main()
