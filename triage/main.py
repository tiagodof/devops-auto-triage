"""
DevOps Auto Triage — main entry point.
Triggered by GitHub Actions on issue open events.
"""
import os
from triage.classifier import classify_issue
from triage.estimator import estimate_complexity
from triage.assignee_suggester import suggest_assignee
from triage.github_client import GitHubClient
from triage.comment_builder import build_triage_comment


def main():
    issue_number = int(os.environ["ISSUE_NUMBER"])
    issue_title  = os.environ.get("ISSUE_TITLE", "")
    issue_body   = os.environ.get("ISSUE_BODY", "")
    repo         = os.environ["REPO_FULL_NAME"]

    client = GitHubClient(token=os.environ["GITHUB_TOKEN"], repo=repo)

    print(f"[triage] Processing issue #{issue_number}: {issue_title}")

    # Step 1 — Classify
    category = classify_issue(title=issue_title, body=issue_body)
    print(f"[triage] Category: {category}")

    # Step 2 — Estimate complexity
    story_points = estimate_complexity(title=issue_title, body=issue_body)
    print(f"[triage] Story points: {story_points}")

    # Step 3 — Suggest assignee
    assignee, reason = suggest_assignee(
        title=issue_title,
        body=issue_body,
        commit_log=client.get_recent_commits(),
    )
    print(f"[triage] Suggested assignee: {assignee} ({reason})")

    # Step 4 — Apply labels
    client.add_labels(issue_number, [category, f"{story_points}sp"])

    # Step 5 — Post triage comment
    comment = build_triage_comment(
        category=category,
        story_points=story_points,
        assignee=assignee,
        reason=reason,
    )
    client.post_comment(issue_number, comment)

    print(f"[triage] Done. Issue #{issue_number} triaged successfully.")


if __name__ == "__main__":
    main()
