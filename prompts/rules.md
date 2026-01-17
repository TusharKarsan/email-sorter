# Global Aider Rules for This Project

## Coding Style
- Use British English spelling (optimise, initialise, colour).
- Use type hints everywhere.
- Use NumPy-style docstrings.
- Prefer functional programming where reasonable.
- Avoid side effects unless explicitly required.
- Keep modules small and cohesive.

## File Boundaries
- Only modify files inside the src/ directory unless explicitly instructed.
- Never create or modify files inside .git/, .venv/, data/, or .continue/.
- Use forward slashes (/) for all Python paths, even on Windows.

## Behaviour
- Explain your reasoning briefly before making changes.
- When refactoring, preserve behaviour unless told otherwise.
- When adding new files, include minimal boilerplate (imports, docstring).
- When updating multiple files, keep changes logically grouped.

## Project Context
- This project runs on Windows (Small_One).
- The remote Design PC hosts Ollama and Qdrant.
- Avoid Docker; use Conda and UVX for tooling.
- Assume the project root is D:/python/email-sorter/.

## Git Rules
- Make small, atomic commits.
- Write clear commit messages describing the change.
- Do not reformat unrelated code unless asked.

## RAG / External Tools
- When relevant, prefer context retrieved from Qdrant.
- When generating embeddings, assume bge-m3 or nomic-embed-text.
- When ranking results, assume Qwen3-Reranker-8B.

## Safety
- Never delete files unless explicitly instructed.
- Never rename directories without confirmation.
