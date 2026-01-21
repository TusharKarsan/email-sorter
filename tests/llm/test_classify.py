import pytest
from src.llm import classify

def test_classify_email_success(mocker):
    """
    Test that classify_email returns a valid category when the API call is successful.
    """
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": '{"category": "Job"}'
    }
    mocker.patch("requests.post", return_value=mock_response)

    # Act
    result = classify.classify_email("This is a job application.")

    # Assert
    assert result == {"category": "Job"}

def test_classify_email_api_error(mocker):
    """
    Test that classify_email returns an error category when the API call fails.
    """
    # Arrange
    mocker.patch("requests.post", side_effect=Exception("API Error"))

    # Act
    result = classify.classify_email("This is a test email.")

    # Assert
    assert result["category"] == "Error"
    assert "API Error" in result["reason"]

def test_classify_email_empty_response(mocker):
    """
    Test that classify_email returns an error category when the API returns an empty response.
    """
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": ""
    }
    mocker.patch("requests.post", return_value=mock_response)

    # Act
    result = classify.classify_email("This is another test email.")

    # Assert
    assert result["category"] == "Error"
    assert "Empty response" in result["reason"]
