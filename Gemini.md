# Gemini AI Assistant Guidelines

This document provides guidelines for interacting with the Gemini AI assistant in the context of the `email-sorter` project.

## Project Overview

The `email-sorter` is a Python application designed to sort emails using a Large Language Model (LLM) for classification. It connects to an IMAP server, processes emails, and uses an LLM to categorize them.

- **`src/`**: Contains the main application logic, including modules for IMAP communication (`imap/`), LLM interaction (`llm/`), and data storage (`storage/`).
- **`scripts/`**: Includes helper scripts for sanity checks and other tasks.
- **`tests/`**: Contains tests for the application (currently empty).
- **`environment.yaml`**: Defines the Python dependencies for the Conda environment.
- **`package.json`**: Defines the Node.js dependencies and scripts.

## Environment Setup

To ensure consistent and reproducible results, please follow these setup instructions.

### Python (Conda)

The project uses a Conda environment named `email-sorter`.

1.  **Create the environment:**
    ```bash
    conda env create -f environment.yaml
    ```
2.  **Activate the environment:**
    ```bash
    conda activate email-sorter
    ```
3.  **Update the environment:** (if `environment.yaml` changes)
    ```bash
    conda env update -f environment.yaml --prune
    ```

### Node.js

The project also uses Node.js for some development scripts.

1.  **Install dependencies:**
    ```bash
    npm install
    ```

## Development Workflow

### Running the Application

The main entry point for the application is `src/main.py`.

### Running Tests

The `tests/` directory is currently empty. You can ask Gemini to help write tests for the application.

**Example Prompt:**
> "Write a unit test for the `src.llm.classify` module."

### Linting and Formatting

The project uses **Black** for Python code formatting. Please ensure that all new code adheres to this standard.

## How to Interact with Gemini

Here are some examples of how you can ask Gemini to help you with this project:

### Understanding the Code

> "Explain the purpose of the `src/imap/client.py` file."
> "Walk me through the `src/main.py` file."

### Adding Features

> "Add a feature to store sorted emails in a SQLite database instead of JSON files."
> "Implement a new classifier using a different LLM."

### Writing Tests

> "Write a test for the `fetch_emails` function in `src/imap/client.py`."
> "Create a test suite for the `src/storage/json_store.py` module."

### Improving Documentation

> "Update the `ReadMe.md` file to include a section on the new database storage feature."
> "Add comments to the `src/llm/classify.py` file to explain the classification logic."

### Debugging

> "I'm getting an error when running `src/main.py`. Here is the error message: `...`. Can you help me debug it?"
