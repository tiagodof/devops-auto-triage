"""
Shared pytest fixtures and helpers for the devops-auto-triage test suite.
"""
import pytest
from unittest.mock import MagicMock


def make_mock_response(content: str):
    """Creates a mock OpenAI chat completion response with the given content."""
    mock = MagicMock()
    mock.choices[0].message.content = content
    return mock


@pytest.fixture
def mock_llm_client():
    """Returns a mock OpenAI client ready to be configured per test."""
    return MagicMock()
