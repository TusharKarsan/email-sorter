# tests/test_rules.py
import pytest
from src.rules import classify_by_rule

def test_classify_by_rule_linkedin_match():
    """Test that a LinkedIn job alert is correctly classified."""
    result = classify_by_rule("jobs-noreply@linkedin.com", "New job alert: Software Engineer")
    assert result is not None
    assert result["category"] == "Job"
    assert "linkedin.com" in result["reason"]

def test_classify_by_rule_cv_library_match():
    """Test that a CV-Library job alert is correctly classified."""
    result = classify_by_rule("jobs@cv-library.co.uk", "Job Alert: Python Developer")
    assert result is not None
    assert result["category"] == "Job"
    assert "cv-library.co.uk" in result["reason"]

def test_classify_by_rule_no_match():
    """Test that an email that doesn't match any rule returns None."""
    result = classify_by_rule("random@example.com", "This is a random email")
    assert result is None

def test_classify_by_rule_case_insensitivity():
    """Test that the rule matching is case-insensitive."""
    result = classify_by_rule("JOBS-NOREPLY@LINKEDIN.COM", "  NEW JOB ALERT: Senior Python Developer  ")
    assert result is not None
    assert result["category"] == "Job"
    assert "linkedin.com" in result["reason"]

def test_classify_by_rule_partial_match_fails():
    """Test that a partial match on subject prefix fails."""
    result = classify_by_rule("jobs-noreply@linkedin.com", "Alert: New job")
    assert result is None
