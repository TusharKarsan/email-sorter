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


def get_classification_prompt_original():
    return """You are classifying emails related to job applications and recruitment.

Your task is to classify the email into EXACTLY ONE of the following categories:

- application_acknowledged
- application_rejected
- job_opportunity
- not_relevant

You MUST follow the decision rules below in order.

DECISION RULES (apply in this exact priority):

1. application_rejected
Classify as "application_rejected" if the email explicitly states or clearly implies that an application was unsuccessful.
Strong signals include phrases such as:
- "we regret to inform you"
- "unfortunately"
- "will not be progressing"
- "unsuccessful"
Polite or encouraging language does NOT override a rejection.

2. application_acknowledged
Classify as "application_acknowledged" if the email clearly refers to an application the candidate submitted and confirms receipt, review, or processing.
Strong signals include:
- "we have received your application"
- "thank you for applying"
- "your application is under review"
There must be NO rejection language present.

3. job_opportunity
Classify as "job_opportunity" if the email initiates contact about a potential role that the candidate did NOT apply for.
Typical characteristics:
- Sent by a recruiter or recruitment agency
- Mentions a client, vacancy, or role matching the candidate's skills
- Asks about interest, availability, or CV
- Does NOT reference an application previously submitted

4. not_relevant
Classify as "not_relevant" if none of the above categories apply.
This includes newsletters, job alerts, recruiter marketing, CV update reminders, or unrelated emails.

TIE-BREAKING:
- Explicit rejection always overrides all other signals.
- If the email references "your application", it cannot be classified as job_opportunity.
- If unsure, choose "not_relevant".

OUTPUT FORMAT:
Return ONLY a valid JSON object in the following format and nothing else:

{"category": "<one_of_the_allowed_categories>"}

EMAIL CONTENT:
{text}
"""
