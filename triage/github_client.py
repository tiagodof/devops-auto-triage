"""
GitHub API client wrapper for DevOps Auto Triage.
"""
import requests


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str, repo: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self.repo = repo

    def post_comment(self, issue_number: int, body: str) -> None:
        url = f"{self.BASE_URL}/repos/{self.repo}/issues/{issue_number}/comments"
        response = requests.post(url, headers=self.headers, json={"body": body})
        response.raise_for_status()
        print(f"[github_client] Comment posted on issue #{issue_number}")

    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        # Ensure labels exist first
        for label in labels:
            self._ensure_label_exists(label)

        url = f"{self.BASE_URL}/repos/{self.repo}/issues/{issue_number}/labels"
        response = requests.post(url, headers=self.headers, json={"labels": labels})
        response.raise_for_status()
        print(f"[github_client] Labels {labels} added to issue #{issue_number}")

    def _ensure_label_exists(self, label: str) -> None:
        url = f"{self.BASE_URL}/repos/{self.repo}/labels"
        color_map = {
            "bug": "d73a4a", "feature": "0075ca", "documentation": "0052cc",
            "question": "d876e3", "security": "e4e669",
        }
        color = color_map.get(label, "ededed")
        requests.post(url, headers=self.headers, json={"name": label, "color": color})

    def get_recent_commits(self, per_page: int = 30) -> list[dict]:
        url = f"{self.BASE_URL}/repos/{self.repo}/commits?per_page={per_page}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return []

        commits = []
        for c in response.json():
            commits.append({
                "author": c["author"]["login"] if c.get("author") else "unknown",
                "message": c["commit"]["message"].split("\n")[0],
                "files": [],
            })
        return commits
