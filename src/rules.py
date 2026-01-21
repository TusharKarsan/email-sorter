# src/rules.py
"""
This module contains rules for pre-classifying emails to bypass the LLM.
"""

RULES = [
    {
        "sender": "linkedin.com",
        "subject_prefix": "New job alert:",
        "category": "Job"
    },
    {
        "sender": "cv-library.co.uk",
        "subject_prefix": "Job Alert:",
        "category": "Job"
    },
    # Add more rules here
]

def classify_by_rule(email_from, subject):
    """
    Classifies an email based on a set of rules.

    Args:
        email_from (str): The sender's email address.
        subject (str): The email subject.

    Returns:
        dict: A dictionary with the category and reason if a rule matches, otherwise None.
    """
    for rule in RULES:
        # Check if the sender is in the from address and the subject starts with the prefix
        if rule["sender"].lower() in email_from.lower() and subject.lower().strip().startswith(rule["subject_prefix"].lower()):
            return {
                "category": rule["category"],
                "reason": f"Rule-based classification for sender '{rule['sender']}'"
            }
    return None
