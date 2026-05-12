"""
DevOps Auto Triage — main entry point.
Triggered by GitHub Actions on issue open events.
"""
import os
import logging
from triage.config_loader import load_config, get_label_colors, get_ai_model
from triage.classifier import classify_issue
from triage.estimator import estimate_complexity
from triage.assignee_suggester import suggest_assignee
from triage.github_client import GitHubClient
from triage.comment_builder import build_triage_comment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def validate_env() -> None:
    """Fail fast with a clear message if required env vars are missing."""
    required = ["GITHUB_TOKEN", "REPO_FULL_NAME", "ISSUE_NUMBER", "OPENAI_API_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


def main():
    validate_env()

    issue_number = int(os.environ["ISSUE_NUMBER"])
    issue_title  = os.environ.get("ISSUE_TITLE", "")
    issue_body   = os.environ.get("ISSUE_BODY", "")
    repo         = os.environ["REPO_FULL_NAME"]

    # Load config — fixes "config never loaded" bug
    config = load_config()
    color_map = get_label_colors(config)
    model = get_ai_model(config)

    client = GitHubClient(
        token=os.environ["GITHUB_TOKEN"],
        repo=repo,
        color_map=color_map,
    )

    logger.info("Processing issue #%d: %s", issue_number, issue_title)

    # Step 1 — Classify
    category = classify_issue(title=issue_title, body=issue_body, model=model)
    logger.info("Category: %s", category)

    # Step 2 — Estimate complexity
    story_points = estimate_complexity(title=issue_title, body=issue_body, model=model)
    logger.info("Story points: %d", story_points)

    # Step 3 — Suggest assignee
    assignee, reason = suggest_assignee(
        title=issue_title,
        body=issue_body,
        commit_log=client.get_recent_commits(),
        model=model,
    )
    logger.info("Suggested assignee: %s (%s)", assignee, reason)

    # Step 4 — Post comment first (independent of label success)
    comment = build_triage_comment(
        category=category,
        story_points=story_points,
        assignee=assignee,
        reason=reason,
    )
    try:
        client.post_comment(issue_number, comment)
    except Exception as e:
        logger.error("Failed to post triage comment: %s", e)

    # Step 5 — Apply labels (failure here no longer blocks the comment)
    try:
        client.add_labels(issue_number, [category, f"{story_points}sp"])
    except Exception as e:
        logger.error("Failed to apply labels: %s", e)

    logger.info("Done. Issue #%d triaged successfully.", issue_number)


if __name__ == "__main__":
    main()
