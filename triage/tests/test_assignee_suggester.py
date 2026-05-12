"""Unit tests for the assignee suggester."""
from unittest.mock import MagicMock
from triage.assignee_suggester import suggest_assignee
from triage.tests.conftest import make_mock_response

SAMPLE_COMMITS = [
    {"author": "tiagodof", "message": "fix: login bug", "files": ["auth/login.py"]},
    {"author": "tiagodof", "message": "feat: add dashboard", "files": ["frontend/App.tsx"]},
]


def _client(content: str) -> MagicMock:
    c = MagicMock()
    c.chat.completions.create.return_value = make_mock_response(content)
    return c


def test_returns_suggested_username():
    username, reason = suggest_assignee(
        "Login bug", "Clicking login does nothing.",
        commit_log=SAMPLE_COMMITS,
        client=_client("tiagodof"),
    )
    assert username == "tiagodof"
    assert reason != ""


def test_strips_at_symbol():
    username, _ = suggest_assignee(
        "Some issue", "Some body",
        commit_log=SAMPLE_COMMITS,
        client=_client("@tiagodof"),
    )
    assert username == "tiagodof"


def test_empty_commit_log_returns_empty():
    username, reason = suggest_assignee("Issue", "Body", commit_log=[])
    assert username == ""
    assert "No commit history" in reason


def test_fallback_on_api_exception():
    c = MagicMock()
    c.chat.completions.create.side_effect = Exception("API error")
    username, reason = suggest_assignee("Issue", "Body", commit_log=SAMPLE_COMMITS, client=c)
    assert username == ""
    assert "Could not determine" in reason
