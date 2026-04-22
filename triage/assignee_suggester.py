"""
Suggests the best developer to assign to an issue
based on commit history and issue content.
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a DevOps assistant that suggests the best developer to assign to a GitHub issue.
You will receive:
1. The issue title and body
2. A list of recent commits with author and changed files

Based on this, suggest the GitHub username of the most relevant developer.
Respond with ONLY the GitHub username (no @ symbol, no explanation)."""


def suggest_assignee(title: str, body: str, commit_log: list[dict]) -> tuple[str, str]:
    """
    Suggest the best assignee for an issue.
    Returns (username, reason).
    """
    if not commit_log:
        return ("", "No commit history available.")

    commits_summary = "\n".join(
        f"- {c['author']}: {c['message']} (files: {', '.join(c.get('files', [])[:3])})"
        for c in commit_log[:20]
    )

    user_message = (
        f"Issue Title: {title}\n"
        f"Issue Body: {body or '(no body)'}\n\n"
        f"Recent Commits:\n{commits_summary}"
    )

    try:
        response = client.chat.completions.create(
            model=os.getenv("AI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=0,
            max_tokens=30,
        )
        username = response.choices[0].message.content.strip().lstrip("@")
        reason = "Matched based on recent commit history and file relevance."
        return (username, reason)
    except Exception as e:
        print(f"[assignee_suggester] Error: {e}")
        return ("", "Could not determine assignee.")
