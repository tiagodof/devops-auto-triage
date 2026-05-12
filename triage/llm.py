"""
Shared LLM helper — eliminates code duplication across classifier,
estimator, and assignee_suggester.

Previously each module instantiated its own global OpenAI client and
duplicated the chat.completions.create call. This module centralises
that logic and supports dependency injection for easier testing.
"""
import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# Default client — can be overridden via dependency injection in tests
_default_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Returns the shared OpenAI client, creating it on first use."""
    global _default_client
    if _default_client is None:
        api_key = os.environ["OPENAI_API_KEY"]  # Raises KeyError immediately if missing
        _default_client = OpenAI(api_key=api_key)
    return _default_client


def call_llm(
    system_prompt: str,
    user_message: str,
    model: str | None = None,
    max_tokens: int = 50,
    client: OpenAI | None = None,
) -> str:
    """
    Makes a single chat completion call with temperature=0.
    Accepts an optional client for dependency injection (useful in tests).
    Returns the raw stripped response string.
    Raises on API errors — callers are responsible for handling exceptions.
    """
    llm = client or get_client()
    resolved_model = model or os.getenv("AI_MODEL", "gpt-4o-mini")

    response = llm.chat.completions.create(
        model=resolved_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        temperature=0,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
