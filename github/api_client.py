# github/api_client.py

import requests
import os

class GitHubAPIClient:
    """
    Basic GitHub API client using a personal access token.
    """

    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("A GitHub personal access token is required")
        self.base_url = "https://api.github.com"

    def _headers(self):
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_issue(self, owner, repo, title, body):
        """
        Create a new issue in the given repository.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        payload = {"title": title, "body": body}
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def create_pull_request(self, owner, repo, head, base, title, body):
        """
        Create a pull request from head to base branch.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        payload = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def comment_on_issue(self, owner, repo, issue_number, comment_body):
        """
        Add a comment to an existing issue.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        payload = {"body": comment_body}
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()
