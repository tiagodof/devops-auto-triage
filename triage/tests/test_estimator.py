"""Unit tests for the story point estimator."""
from unittest.mock import patch, MagicMock
from triage.estimator import estimate_complexity, STORY_POINTS


def make_mock_response(content: str):
    mock = MagicMock()
    mock.choices[0].message.content = content
    return mock


@patch("triage.estimator.client")
def test_estimate_returns_valid_point(mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response("5")
    result = estimate_complexity("Add OAuth2 login", "Implement Google OAuth2 flow.")
    assert result == 5
    assert result in STORY_POINTS


@patch("triage.estimator.client")
def test_estimate_fallback_on_invalid(mock_client):
    mock_client.chat.completions.create.return_value = make_mock_response("99")
    result = estimate_complexity("Some issue", "Some body")
    assert result == 3  # fallback default
