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

def get_classification_prompt(email_text: str) -> str:
    return f"""You are classifying emails related to job applications and recruitment.

Your task is to classify the email into EXACTLY ONE of the following categories:
- application_acknowledged
- application_rejected
- job_opportunity
- not_relevant

Follow the DECISION RULES in order (rejection > acknowledged > opportunity > not relevant).

OUTPUT FORMAT:
Return ONLY a valid JSON object in this format and nothing else:
{{"category": "<one_of_the_allowed_categories>", "confidence": <0-1>, "rationale": "<brief explanation>"}}.

EMAIL CONTENT:
{email_text}

Do NOT include any commentary or extra text. Only return the JSON object."""
