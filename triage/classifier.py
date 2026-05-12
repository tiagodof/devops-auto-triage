"""
AI-powered issue classifier.
Classifies GitHub issues into: bug, feature, documentation, question, security.
"""
import logging
from openai import OpenAI
from triage.llm import call_llm

logger = logging.getLogger(__name__)

CATEGORIES = ["bug", "feature", "documentation", "question", "security"]

SYSTEM_PROMPT = """You are a software engineering assistant that classifies GitHub issues.
Given an issue title and body, respond with ONLY one of these categories (lowercase, no punctuation):
bug, feature, documentation, question, security

Rules:
- bug: something is broken or not working as expected
- feature: a new capability or enhancement is requested
- documentation: relates to docs, README, comments, or examples
- question: asking for help, clarification, or guidance
- security: vulnerability, CVE, authentication, or data exposure concern

Respond with exactly one word."""


def classify_issue(
    title: str,
    body: str,
    model: str | None = None,
    client: OpenAI | None = None,
) -> str:
    """Classify a GitHub issue using an LLM. Returns one of CATEGORIES."""
    # Sanitise inputs: truncate to prevent prompt injection
    safe_title = title[:200]
    safe_body  = (body or "")[:2000]
    user_message = f"Title: {safe_title}\n\nBody: {safe_body or '(no body provided)'}"

    try:
        result = call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_message=user_message,
            model=model,
            max_tokens=10,
            client=client,
        ).lower()
        return result if result in CATEGORIES else "question"
    except Exception as e:
        logger.error("classify_issue failed: %s — returning fallback 'question'", e)
        return "question"
