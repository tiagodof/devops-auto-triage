"""
AI-powered story point estimator.
Uses Fibonacci scale: 1, 2, 3, 5, 8, 13
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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


def estimate_complexity(title: str, body: str) -> int:
    """Estimate story points for a GitHub issue using an LLM."""
    user_message = f"Title: {title}\n\nBody: {body or '(no body provided)'}"

    try:
        response = client.chat.completions.create(
            model=os.getenv("AI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=0,
            max_tokens=5,
        )
        result = int(response.choices[0].message.content.strip())
        return result if result in STORY_POINTS else 3
    except Exception as e:
        print(f"[estimator] Error: {e}")
        return 3
