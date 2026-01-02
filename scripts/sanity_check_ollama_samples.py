# src/scripts/sanity_check_ollama_samples.py
"""
Sanity check for passing sample .eml emails through Ollama / LLM.
- Uses classify_email() from llm/classify.py
- Prints category + body preview
"""

from pathlib import Path
from src.llm.classify import classify_email
from src.imap.parser import parse_rfc822

def preview_text(text: str, length: int = 120) -> str:
    """Return first `length` characters of text for preview"""
    text = text.replace("\n", " ").strip()
    return (text[:length] + "...") if len(text) > length else text

def main():
    emails_dir = Path("data/samples/eml")
    if not emails_dir.exists():
        print(f"Emails directory not found: {emails_dir}")
        return

    eml_files = sorted(emails_dir.glob("*.eml"))
    if not eml_files:
        print(f"No .eml files found in {emails_dir}")
        return

    for idx, eml_file in enumerate(eml_files, start=1):
        with open(eml_file, "rb") as f:
            raw_data = f.read()

        parsed = parse_rfc822(raw_data)

        try:
            classification = classify_email(parsed["body"])
        except Exception as e:
            classification = f"Failed: {e}"

        body_preview = preview_text(parsed["body"], 120)

        print("="*80)
        print(f"{idx:02d} {eml_file.name}")
        print(f"FROM       : {parsed['from']}")
        print(f"SUBJECT    : {parsed['subject']}")
        print(f"DATE       : {parsed['date']}")
        print(f"BODY LEN   : {len(parsed['body'])}")
        print(f"CLASSIFICATION:\n{classification}")
        print(f"PREVIEW    : {body_preview}")

if __name__ == "__main__":
    main()
