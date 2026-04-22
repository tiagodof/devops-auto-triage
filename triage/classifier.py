"""
AI-powered issue classifier.
Classifies GitHub issues into: bug, feature, documentation, question, security.
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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


def classify_issue(title: str, body: str) -> str:
    """Classify a GitHub issue using an LLM."""
    user_message = f"Title: {title}\n\nBody: {body or '(no body provided)'}"

    try:
        response = client.chat.completions.create(
            model=os.getenv("AI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=0,
            max_tokens=10,
        )
        result = response.choices[0].message.content.strip().lower()
        return result if result in CATEGORIES else "question"
    except Exception as e:
        print(f"[classifier] Error: {e}")
        return "question"
