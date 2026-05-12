"""
Suggests the best developer to assign to an issue
based on commit history and issue content.
"""
import logging
from openai import OpenAI
from triage.llm import call_llm

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a DevOps assistant that suggests the best developer to assign to a GitHub issue.
You will receive:
1. The issue title and body
2. A list of recent commits with author and changed files

Based on this, suggest the GitHub username of the most relevant developer.
Respond with ONLY the GitHub username (no @ symbol, no explanation)."""


def suggest_assignee(
    title: str,
    body: str,
    commit_log: list[dict],
    model: str | None = None,
    client: OpenAI | None = None,
) -> tuple[str, str]:
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

    safe_title = title[:200]
    safe_body  = (body or "")[:2000]

    user_message = (
        f"Issue Title: {safe_title}\n"
        f"Issue Body: {safe_body or '(no body)'}\n\n"
        f"Recent Commits:\n{commits_summary}"
    )

    try:
        username = call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_message=user_message,
            model=model,
            max_tokens=30,
            client=client,
        ).lstrip("@")
        reason = "Matched based on recent commit history and file relevance."
        return (username, reason)
    except Exception as e:
        logger.error("suggest_assignee failed: %s", e)
        return ("", "Could not determine assignee.")
