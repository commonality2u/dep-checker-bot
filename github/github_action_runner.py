# github/github_action_runner.py

import os
import logging
from github.api_client import GitHubAPIClient
from audit.auto_pr_generator import create_pull_request
from audit.report_generator import generate_report  # Ejemplo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_env_variable(var_name):
    """
    Helper function to get environment variables and handle missing ones.
    """
    value = os.getenv(var_name)
    if not value:
        logger.error(f"Missing required environment variable: {var_name}")
    return value

def run_report_and_issue(client, owner, repo):
    """
    Generate a dependency report and create an issue on GitHub.
    """
    try:
        report = generate_report()
        logger.info("Dependency report generated successfully.")
        logger.debug(f"Generated report content:\n{report}")

        issue = client.create_issue(
            owner=owner,
            repo=repo,
            title="Dependency Report",
            body=report
        )
        logger.info(f"Issue created successfully: {issue['html_url']}")
    except Exception as e:
        logger.error(f"Error while generating report and creating issue: {e}")


def run_auto_pr(client, owner, repo):
    """
    Run the automatic PR generation.
    """
    try:
        pr = create_pull_request(
            github_token=client.token,
            repo_name=f"{owner}/{repo}",
            base_branch="main",
            head_branch="audit/update-dependencies",
            files_to_commit=["audit_report.json", "badge.svg"],  # ajusta según tus archivos reales
            commit_message="Update dependencies",
            pr_title="Auto PR - Dependency Update",
            pr_body="Automated PR with updated dependencies."
        )
        if pr:
            logger.info(f"Pull request created successfully: {pr.html_url}")
        else:
            logger.warning("No pull request was created.")
    except Exception as e:
        logger.error(f"Error creating pull request: {e}")

def main():
    """
    Entry point to run actions from a GitHub Action or locally.
    """
    github_token = get_env_variable("GITHUB_TOKEN")
    repo_owner = get_env_variable("GITHUB_REPO_OWNER")
    repo_name = get_env_variable("GITHUB_REPO_NAME")

    if not all([github_token, repo_owner, repo_name]):
        logger.error("One or more required environment variables are missing. Exiting.")
        return

    client = GitHubAPIClient(token=github_token)

    # Run tasks
    run_report_and_issue(client, repo_owner, repo_name)
    run_auto_pr(client, repo_owner, repo_name)

if __name__ == "__main__":
    main()
# This script is intended to be run as a GitHub Action or locally.
# It uses environment variables to get the GitHub token and repository details.
# Make sure to set these environment variables in your GitHub Action workflow or local environment.
# You can extend this script to include more actions as needed.
# Ensure you have the necessary permissions for the GitHub token to create issues and pull requests.