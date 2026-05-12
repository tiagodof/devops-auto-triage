"""
GitHub API client wrapper for DevOps Auto Triage.
Includes retry logic with exponential backoff for transient failures.
"""
import time
import logging
import requests

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds


def _request_with_retry(method: str, url: str, headers: dict, **kwargs) -> requests.Response:
    """
    Wraps requests calls with simple exponential backoff retry.
    Retries on 429 (rate limit) and 5xx (server errors).
    """
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code in (429, 500, 502, 503, 504):
            wait = BACKOFF_BASE ** attempt
            logger.warning(
                "Request to %s returned %d, retrying in %ds (attempt %d/%d)",
                url, response.status_code, wait, attempt, MAX_RETRIES,
            )
            time.sleep(wait)
            continue
        return response
    return response  # return last response after exhausting retries


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str, repo: str, color_map: dict | None = None):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self.repo = repo
        self.color_map = color_map or {
            "bug": "d73a4a", "feature": "0075ca", "documentation": "0052cc",
            "question": "d876e3", "security": "e4e669",
        }

    def post_comment(self, issue_number: int, body: str) -> None:
        url = f"{self.BASE_URL}/repos/{self.repo}/issues/{issue_number}/comments"
        response = _request_with_retry("POST", url, self.headers, json={"body": body})
        response.raise_for_status()
        logger.info("Comment posted on issue #%d", issue_number)

    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        for label in labels:
            self._ensure_label_exists(label)
        url = f"{self.BASE_URL}/repos/{self.repo}/issues/{issue_number}/labels"
        response = _request_with_retry("POST", url, self.headers, json={"labels": labels})
        response.raise_for_status()
        logger.info("Labels %s added to issue #%d", labels, issue_number)

    def _ensure_label_exists(self, label: str) -> None:
        url = f"{self.BASE_URL}/repos/{self.repo}/labels"
        color = self.color_map.get(label, "ededed")
        _request_with_retry("POST", url, self.headers, json={"name": label, "color": color})

    def get_recent_commits(self, per_page: int = 20) -> list[dict]:
        """
        Fetches recent commits including the files changed in each one.
        Makes one extra API call per commit to retrieve file details.
        """
        list_url = f"{self.BASE_URL}/repos/{self.repo}/commits?per_page={per_page}"
        response = _request_with_retry("GET", list_url, self.headers)
        if response.status_code != 200:
            logger.warning("Could not fetch commits: %d", response.status_code)
            return []

        commits = []
        for c in response.json():
            sha    = c["sha"]
            author  = c["author"]["login"] if c.get("author") else "unknown"
            message = c["commit"]["message"].split("\n")[0]
            files   = self._get_commit_files(sha)
            commits.append({"author": author, "message": message, "files": files})
        return commits

    def _get_commit_files(self, sha: str) -> list[str]:
        """Returns the list of filenames changed in a single commit."""
        url = f"{self.BASE_URL}/repos/{self.repo}/commits/{sha}"
        response = _request_with_retry("GET", url, self.headers)
        if response.status_code != 200:
            return []
        return [f["filename"] for f in response.json().get("files", [])]
