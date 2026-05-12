"""
Input sanitisation for issue titles and bodies.
Prevents prompt injection by truncating inputs and stripping
patterns commonly used to override system prompts.
"""
import re
import logging

logger = logging.getLogger(__name__)

MAX_TITLE_LEN = 200
MAX_BODY_LEN  = 2000

INJECTION_PATTERNS = [
    r"ignore (all |previous |above )?instructions",
    r"disregard (all |previous |above )?instructions",
    r"you are now",
    r"new system prompt",
    r"forget everything",
    r"act as",
]

_INJECTION_RE = re.compile(
    "|".join(INJECTION_PATTERNS),
    flags=re.IGNORECASE,
)


def sanitise(text: str, max_len: int) -> str:
    """
    Truncates text to max_len and removes known prompt injection patterns.
    Returns the cleaned string.
    """
    if not text:
        return ""

    truncated = text[:max_len]

    if _INJECTION_RE.search(truncated):
        logger.warning("Potential prompt injection detected in input, patterns removed.")
        truncated = _INJECTION_RE.sub("[removed]", truncated)

    return truncated


def sanitise_issue(title: str, body: str) -> tuple[str, str]:
    """Sanitises both title and body of a GitHub issue."""
    return sanitise(title, MAX_TITLE_LEN), sanitise(body, MAX_BODY_LEN)
