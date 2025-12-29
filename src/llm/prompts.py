# llm/prompts.py
"""
Responsibilities:
- Define the classification prompt used by the LLM
- Enumerate allowed categories explicitly
- Instruct the model to return STRICT JSON only
- Avoid any application logic or API calls
- Prompt should be deterministic and concise
- Only return a prompt string; do not implement classification or parsing
"""

def get_classification_prompt():
    return """Classify the following text into one of these categories only:
- 'technology'
- 'health'
- 'finance'
- 'education'
- 'entertainment'
- 'sports'
- 'politics'
- 'science'
- 'business'
- 'travel'

Return ONLY a valid JSON object with the key 'category' and the value being the selected category from the list above.
Example:
{"category": "technology"}

Text: {text}"""
