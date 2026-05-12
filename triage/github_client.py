"""
GitHub API client wrapper for DevOps Auto Triage.
"""
import logging
import requests

logger = logging.getLogger(__name__)


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str, repo: str, color_map: dict | None = None):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self.repo = repo
        # Allow color map to be injected from config instead of hardcoded
        self.color_map = color_map or {
            "bug": "d73a4a", "feature": "0075ca", "documentation": "0052cc",
            "question": "d876e3", "security": "e4e669",
        }

    def post_comment(self, issue_number: int, body: str) -> None:
        url = f"{self.BASE_URL}/repos/{self.repo}/issues/{issue_number}/comments"
        response = requests.post(url, headers=self.headers, json={"body": body})
        response.raise_for_status()
        logger.info("Comment posted on issue #%d", issue_number)

    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        for label in labels:
            self._ensure_label_exists(label)
        url = f"{self.BASE_URL}/repos/{self.repo}/issues/{issue_number}/labels"
        response = requests.post(url, headers=self.headers, json={"labels": labels})
        response.raise_for_status()
        logger.info("Labels %s added to issue #%d", labels, issue_number)

    def _ensure_label_exists(self, label: str) -> None:
        url = f"{self.BASE_URL}/repos/{self.repo}/labels"
        color = self.color_map.get(label, "ededed")
        requests.post(url, headers=self.headers, json={"name": label, "color": color})

    def get_recent_commits(self, per_page: int = 20) -> list[dict]:
        """
        Fetches recent commits including the files changed in each one.
        Requires one extra API call per commit to retrieve file details.
        """
        list_url = f"{self.BASE_URL}/repos/{self.repo}/commits?per_page={per_page}"
        response = requests.get(list_url, headers=self.headers)
        if response.status_code != 200:
            logger.warning("Could not fetch commits: %s", response.status_code)
            return []

        commits = []
        for c in response.json():
            sha = c["sha"]
            author = c["author"]["login"] if c.get("author") else "unknown"
            message = c["commit"]["message"].split("\n")[0]

            # Fetch per-commit file details (fixes silent empty-files bug)
            files = self._get_commit_files(sha)

            commits.append({
                "author": author,
                "message": message,
                "files": files,
            })
        return commits

    def _get_commit_files(self, sha: str) -> list[str]:
        """Returns the list of filenames changed in a single commit."""
        url = f"{self.BASE_URL}/repos/{self.repo}/commits/{sha}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return []
        data = response.json()
        return [f["filename"] for f in data.get("files", [])]
