# How DevOps Auto Triage Works

## Overview

When a new issue is opened in a repository where DevOps Auto Triage is installed,
a GitHub Actions workflow is triggered automatically. The workflow runs a Python script
that performs four sequential AI-powered steps.

## Step 1 — Classification

The issue title and body are sent to an LLM with a strict classification prompt.
The model responds with exactly one of: `bug`, `feature`, `documentation`, `question`, `security`.

## Step 2 — Complexity Estimation

The same issue content is sent to the LLM again, this time with a prompt that asks
for a Fibonacci story point estimate (1, 2, 3, 5, 8, or 13). The model is instructed
to respond with only the number.

## Step 3 — Assignee Suggestion

The last 30 commits from the repository are fetched via the GitHub API. The LLM receives
the issue content alongside a summary of recent commits (author + message + changed files)
and suggests the most relevant developer.

## Step 4 — Posting the Triage Report

A formatted Markdown comment is posted on the issue with the classification, story points,
suggested assignee, and priority level. Labels are also applied automatically.

## Example Output

```markdown
## 🤖 AI Triage Report

| Field         | Value                                         |
|---------------|-----------------------------------------------|
| Category      | 🐛 `bug`                                      |
| Complexity    | `3` story points — Medium                     |
| Priority      | 🟠 Medium                                     |
| Suggested Assignee | @tiagodof — Matched based on commit history |
```
