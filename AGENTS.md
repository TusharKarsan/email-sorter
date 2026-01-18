# Email Sorter Project

This is a Python-based utility for categorizing and moving emails via IMAP.

## Project Structure
- `src/main.py`: Entry point for the service loop.
- `src/imap/`: Contains the IMAP client and connection logic.
- `src/logic/`: Folder for sorting rules and AI-based classification.

## Tech Stack
- **Language**: Python 3.10+
- **Protocol**: IMAP (using `imaplib` or `imbox`)
- **Intelligence**: Local Ollama (Qwen 2.5/3.0)

## Development Rules
- Use type hints for all new functions.
- Prefer `pathlib` over `os.path`.
- When adding sorting rules, update the `rules.json` file.
- **Tests**: Run using `pytest`.

## Commands
- **Install**: `pip install -r requirements.txt`
- **Run**: `python src/main.py`
- **Test**: `pytest`
