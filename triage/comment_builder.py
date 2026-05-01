"""
Builds the formatted triage comment to be posted on GitHub issues.
Includes priority suggestion based on category and story points.
"""

COMPLEXITY_LABELS = {
    1: "Trivial", 2: "Simple", 3: "Medium", 5: "Medium-Large", 8: "Large", 13: "Epic"
}

CATEGORY_ICONS = {
    "bug": "🐛", "feature": "✨", "documentation": "📚",
    "question": "❓", "security": "🔒",
}

PRIORITY_MAP = {
    "security":      "🔴 High",
    "bug":           "🟠 Medium",
    "feature":       "🟡 Normal",
    "documentation": "🟢 Low",
    "question":      "🟢 Low",
}


def get_priority(category: str, story_points: int) -> str:
    base = PRIORITY_MAP.get(category, "🟡 Normal")
    if story_points >= 8 and category != "security":
        return "🟠 Medium"
    return base


def build_triage_comment(
    category: str,
    story_points: int,
    assignee: str,
    reason: str,
) -> str:
    icon = CATEGORY_ICONS.get(category, "🏷️")
    complexity_label = COMPLEXITY_LABELS.get(story_points, "Unknown")
    assignee_line = (
        f"@{assignee} — {reason}" if assignee
        else f"_(could not determine)_ — {reason}"
    )
    priority = get_priority(category, story_points)

    return f"""## 🤖 AI Triage Report

| Field | Value |
|---|---|
| **Category** | {icon} `{category}` |
| **Complexity** | `{story_points}` story points _{complexity_label}_ |
| **Priority** | {priority} |
| **Suggested Assignee** | {assignee_line} |

---

_This triage was generated automatically by [DevOps Auto Triage](https://github.com/tiagodof/devops-auto-triage). \
Please review and adjust as needed._

> ⚠️ AI suggestions are a starting point, not a final decision. Always validate with your team.
"""
