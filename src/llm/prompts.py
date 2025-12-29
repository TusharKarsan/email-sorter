# llm/prompts.py
"""
Responsibilities:
- Define the classification prompt used by the LLM
- Enumerate allowed categories explicitly
- Instruct the model to return STRICT JSON only
- Avoid any application logic or API calls
- Prompt should be deterministic and concise
"""

from typing import List


class PromptConfig:
    """
    Configuration for classification prompts.
    """

    def __init__(self, allowed_categories: List[str]):
        self.allowed_categories = allowed_categories


def build_classification_prompt(text: str, prompt_config: PromptConfig) -> str:
    """
    Build the classification prompt used by the LLM.

    Responsibilities:
    - Enumerate allowed categories explicitly
    - Instruct the model to return STRICT JSON only
    - Be deterministic and concise
    """

    categories = ", ".join(prompt_config.allowed_categories)

    prompt = (
        "You are an email classifier.\n\n"
        f"Allowed categories: {categories}\n\n"
        "Classify the email content below into exactly one of the allowed categories.\n"
        "Return ONLY valid JSON in the following format:\n"
        '{ "category": "<one category>", "confidence": <number between 0 and 1> }\n\n'
        "Email content:\n"
        f"{text}"
    )

    return prompt
