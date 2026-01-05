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

# --- 
# Simple version of the classification prompt with details.
# Removed from details:
#    "date_received": "<ISO-8601 date string or null>"
# --- 
def get_classification_prompt(email_text: str) -> str:
    return f"""You are classifying emails related to job applications and recruitment.

Your task is to classify the email into EXACTLY ONE of the following categories:
- application_acknowledged
- application_rejected
- job_opportunity
- not_relevant

Follow the DECISION RULES in order:
1. application_rejected
2. application_acknowledged
3. job_opportunity
4. not_relevant

EXTRACTION RULES:
- ONLY extract employer/recruiter name and job title when the category is
  application_acknowledged OR application_rejected.
- If a requested field is not explicitly found in the email, return null.
- Do NOT infer or guess missing information.

OUTPUT FORMAT:
Return ONLY a valid JSON object in the following structure and nothing else:

{{
  "category": "<one_of_the_allowed_categories>",
  "confidence": <number between 0 and 1>,
  "rationale": "<brief explanation>",
  "employer_or_recruiter": "<string or null>",
  "job_title": "<string or null>"
}}

CONDITIONAL RULE:
- If the category is job_opportunity or not_relevant, the "details" object MUST still be present,
  but all of its fields MUST be null.

EMAIL CONTENT:
{email_text}

Do NOT include any commentary or extra text. Only return the JSON object."""


# --- 
# Simple version of the classification prompt without details.
# --- 
def get_classification_prompt_without_details(email_text: str) -> str:
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
