"""Unit tests for the issue classifier."""
from unittest.mock import MagicMock
from triage.classifier import classify_issue, CATEGORIES
from triage.tests.conftest import make_mock_response


def _client(content: str) -> MagicMock:
    c = MagicMock()
    c.chat.completions.create.return_value = make_mock_response(content)
    return c


def test_classify_bug():
    result = classify_issue("Login button not working", "Clicking login does nothing.", client=_client("bug"))
    assert result == "bug"


def test_classify_feature():
    result = classify_issue("Add dark mode", "Please add a dark mode option.", client=_client("feature"))
    assert result == "feature"


def test_classify_security():
    result = classify_issue("SQL injection in search", "User input not sanitised.", client=_client("security"))
    assert result == "security"


def test_fallback_on_invalid_response():
    result = classify_issue("Some issue", "Some body", client=_client("invalid_category"))
    assert result == "question"


def test_fallback_on_api_exception():
    c = MagicMock()
    c.chat.completions.create.side_effect = Exception("API timeout")
    result = classify_issue("Some issue", "Some body", client=c)
    assert result == "question"


def test_all_valid_categories():
    for category in CATEGORIES:
        result = classify_issue("title", "body", client=_client(category))
        assert result == category
