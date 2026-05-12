"""
AI-powered story point estimator.
Uses Fibonacci scale: 1, 2, 3, 5, 8, 13.
"""
import logging
from openai import OpenAI
from triage.llm import call_llm

logger = logging.getLogger(__name__)

STORY_POINTS = [1, 2, 3, 5, 8, 13]

SYSTEM_PROMPT = """You are a senior software engineer estimating the complexity of GitHub issues.
Use the Fibonacci story point scale: 1, 2, 3, 5, 8, 13.

Guidelines:
- 1 pt: Trivial change, typo fix, config update
- 2 pt: Simple bug fix or small UI change
- 3 pt: Moderate bug fix or small feature
- 5 pt: Medium feature or complex bug
- 8 pt: Large feature or architectural change
- 13 pt: Epic-level work, needs breaking down

Respond with ONLY the number (e.g., 3). No explanation."""


def estimate_complexity(
    title: str,
    body: str,
    model: str | None = None,
    client: OpenAI | None = None,
) -> int:
    """Estimate story points for a GitHub issue. Returns a Fibonacci number."""
    safe_title = title[:200]
    safe_body  = (body or "")[:2000]
    user_message = f"Title: {safe_title}\n\nBody: {safe_body or '(no body provided)'}"

    try:
        raw = call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_message=user_message,
            model=model,
            max_tokens=5,
            client=client,
        )
        # Validate format before casting to avoid confusing ValueError
        if not raw.isdigit():
            logger.warning("Estimator received non-numeric response '%s' — using fallback", raw)
            return 3
        result = int(raw)
        return result if result in STORY_POINTS else 3
    except Exception as e:
        logger.error("estimate_complexity failed: %s — returning fallback 3", e)
        return 3
