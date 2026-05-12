"""Unit tests for the story point estimator."""
from unittest.mock import MagicMock
from triage.estimator import estimate_complexity, STORY_POINTS
from triage.tests.conftest import make_mock_response


def _client(content: str) -> MagicMock:
    c = MagicMock()
    c.chat.completions.create.return_value = make_mock_response(content)
    return c


def test_estimate_returns_valid_point():
    result = estimate_complexity("Add OAuth2 login", "Implement Google OAuth2 flow.", client=_client("5"))
    assert result == 5
    assert result in STORY_POINTS


def test_estimate_trivial():
    result = estimate_complexity("Fix typo in README", "", client=_client("1"))
    assert result == 1


def test_fallback_on_invalid_number():
    result = estimate_complexity("Some issue", "Some body", client=_client("99"))
    assert result == 3


def test_fallback_on_non_numeric_response():
    result = estimate_complexity("Some issue", "Some body", client=_client("medium"))
    assert result == 3


def test_fallback_on_api_exception():
    c = MagicMock()
    c.chat.completions.create.side_effect = Exception("Rate limit exceeded")
    result = estimate_complexity("Some issue", "Some body", client=c)
    assert result == 3


def test_all_valid_story_points():
    for sp in STORY_POINTS:
        result = estimate_complexity("title", "body", client=_client(str(sp)))
        assert result == sp
