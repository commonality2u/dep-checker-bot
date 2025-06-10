# github/api_client.py

import requests
import os
import time
import datetime
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
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
    
    def _handle_response(self, response):
        """
        Handles the response from GitHub API, raising a detailed error if needed.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"GitHub API error: {e} - {response.text}")
            raise

    def create_issue(self, owner, repo, title, body):
        """
        Create a new issue in the given repository.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        payload = {"title": title, "body": body}
        response = requests.post(url, headers=self._headers(), json=payload)
        return self._handle_response(response)

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
        return self._handle_response(response)

    def comment_on_issue(self, owner, repo, issue_number, comment_body):
        """
        Add a comment to an existing issue.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        payload = {"body": comment_body}
        response = requests.post(url, headers=self._headers(), json=payload)
        return self._handle_response(response)
    
    def _check_rate_limit(self, response):
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset_timestamp = response.headers.get("X-RateLimit-Reset")
        if remaining is not None and int(remaining) == 0:
            reset_time = datetime.datetime.fromtimestamp(int(reset_timestamp))
            sleep_seconds = (reset_time - datetime.datetime.now()).total_seconds()
            logger.warning(f"Rate limit exceeded. Sleeping until {reset_time} (about {int(sleep_seconds)} seconds).")

            time.sleep(max(sleep_seconds, 0))
    
    def get_issues(self, owner, repo, state="open"):
        """
        Get a list of issues from the given repository.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        response = requests.get(url, headers=self._headers(), params=params)
        self._check_rate_limit(response)
        return self._handle_response(response)
    
