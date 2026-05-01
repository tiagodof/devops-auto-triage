"""Unit tests for the issue classifier."""
import pytest
from unittest.mock import patch, MagicMock
from triage.classifier import classify_issue, CATEGORIES


def make_mock_response(content: str):
    mock = MagicMock()
    mock.choices[0].message.content = content
    return mock


@patch("triage.classifier.client")
def test_classify_bug(mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response("bug")
    result = classify_issue("Login button not working", "Clicking login does nothing.")
    assert result == "bug"


@patch("triage.classifier.client")
def test_classify_feature(mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response("feature")
    result = classify_issue("Add dark mode", "Please add a dark mode option.")
    assert result == "feature"


@patch("triage.classifier.client")
def test_fallback_on_invalid_response(mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response("invalid_category")
    result = classify_issue("Some issue", "Some body")
    assert result == "question"  # fallback
