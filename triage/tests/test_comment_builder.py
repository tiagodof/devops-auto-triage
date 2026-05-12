"""Unit tests for the triage comment builder."""
from triage.comment_builder import build_triage_comment, get_priority


def test_comment_contains_category():
    comment = build_triage_comment("bug", 3, "tiagodof", "Matched by commit history.")
    assert "bug" in comment


def test_comment_contains_story_points():
    comment = build_triage_comment("feature", 5, "tiagodof", "Matched by commit history.")
    assert "5" in comment


def test_comment_contains_assignee():
    comment = build_triage_comment("bug", 3, "tiagodof", "Matched by commit history.")
    assert "@tiagodof" in comment


def test_comment_handles_no_assignee():
    comment = build_triage_comment("question", 2, "", "No commit history available.")
    assert "could not determine" in comment


def test_priority_security_is_always_high():
    assert get_priority("security", 1) == "🔴 High"
    assert get_priority("security", 13) == "🔴 High"


def test_priority_large_bug_stays_medium():
    assert get_priority("bug", 8) == "🟠 Medium"


def test_priority_feature_normal():
    assert get_priority("feature", 3) == "🟡 Normal"


def test_priority_docs_low():
    assert get_priority("documentation", 1) == "🟢 Low"
