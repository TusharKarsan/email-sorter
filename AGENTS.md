# Agent Guide: Email Sorter Project

## 🎯 Project Mission
A Python-based utility to automatically categorise and organise emails via IMAP, leveraging local LLMs for intelligent classification.

## 🏗️ Architecture & Infrastructure
This project runs across a dual-PC local network:
- **Client (Small_One):** Development environment (Windows/Miniforge3).
- **Server (design):** High-performance backend hosting Ollama and Qdrant.
  - **GPU:** NVIDIA GeForce RTX 3060 (12GB VRAM).
  - **Models:** - `qwen2.5-coder:14b` (Primary reasoning/refactoring).
    - `qwen2.5-coder:7b` (Autocomplete/Quick tasks).
    - `bge-m3` (Embeddings for RAG).

### System Constraints
- **Context Limit:** 24,000 tokens (Optimised for 12GB VRAM).
- **Encoding:** Always use UTF-8 (Fixed Unicode crashes on Windows).
- **Language:** Strictly **British English** (e.g., categorise, organisation).

## 📂 Key File Map
- `src/main.py`: Entry point; contains the 5-minute polling loop and UTF-8 terminal reconfig.
- `src/imap/client.py`: Handles connection to the mail server.
- `src/llm/classify.py`: Bridges the local logic to the `design:11434` API.
- `opencode.json`: Project-specific configuration for the OpenCode agent.

## 🛠️ Development Rules
1. **JSON Safety:** When calling the LLM, always use `"format": "json"` and wrap calls in a `try-except` block to handle `JSONDecodeError`.
2. **Error Handling:** Use the `@retry` decorator or manual retry logic for network-dependent functions.
3. **Pathing:** Use `pathlib` for all file operations to ensure cross-platform compatibility between Windows and WSL.
4. **Documentation:** Use Mermaid diagrams in Obsidian for any new logic flows.

## 🆘 Troubleshooting (Local AI)

### 1. Timeout Errors
If the agent times out (Error: `undefined/chat/completions`), check:
- Is Ollama serving on `design`? (Run `ollama ps`).
- Is the 14b model offloading to CPU? (Should be 100% GPU).
- **Action:** Restart the Ollama service on `design` using the `startup.cmd` script.

### 2. Unicode/Charmap Crashes
If the terminal crashes on emojis (❌/✅):
- Ensure `sys.stdout.reconfigure(encoding='utf-8')` is at the top of the script.
- Check that `SET PYTHONUTF8=1` is set in the shell environment.

### 3. VRAM Exhaustion
If Ollama becomes unresponsive:
- **Action:** Lower the context window in `opencode.json` from `24000` to `16000` to free up the KV Cache.
