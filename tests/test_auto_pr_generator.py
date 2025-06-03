# tests/test_auto_pr_generator.py

import unittest
from unittest.mock import patch, MagicMock
from audit import auto_pr_generator

class TestAutoPRGenerator(unittest.TestCase):
    @patch("audit.auto_pr_generator.Github")
    def test_create_pull_request_success(self, mock_github):
        # Configurar el mock de Github y Repo
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_pr.html_url = "https://github.com/example/repo/pull/1"
        mock_repo.create_pull.return_value = mock_pr
        mock_repo.get_branch.side_effect = [Exception("Branch not found"), MagicMock(commit=MagicMock(sha="abc123"))]
        mock_github.return_value.get_repo.return_value = mock_repo

        result = auto_pr_generator.create_pull_request(
            github_token="fake_token",
            repo_name="user/repo",
            files_to_commit=None,
            reviewers=["usuario1"],
            labels=["audit"],
            draft=True,
            min_health_score=None,
            health_score=70
        )

        self.assertIsNotNone(result)
        mock_repo.create_pull.assert_called_once()
        args, kwargs = mock_repo.create_pull.call_args
        self.assertEqual(kwargs["draft"], True)
        self.assertEqual(kwargs["title"], "Audit Report: Update Dependencies")

        # Revisar reviewers y labels
        mock_pr.create_review_request.assert_called_with(reviewers=["usuario1"])
        mock_pr.add_to_labels.assert_called_with("audit")

    @patch("audit.auto_pr_generator.Github")
    def test_create_pull_request_skips_by_health_score(self, mock_github):
        mock_repo = MagicMock()
        mock_github.return_value.get_repo.return_value = mock_repo

        result = auto_pr_generator.create_pull_request(
            github_token="fake_token",
            repo_name="user/repo",
            min_health_score=85,
            health_score=90
        )
        self.assertIsNone(result)
        mock_repo.create_pull.assert_not_called()

    @patch("audit.auto_pr_generator.Github")
    def test_create_pull_request_authentication_error(self, mock_github):
        mock_github.return_value.get_repo.side_effect = Exception("401 Unauthorized")
        with self.assertLogs(level="ERROR") as log:
            result = auto_pr_generator.create_pull_request(
                github_token="invalid_token",
                repo_name="user/repo"
            )
        self.assertIsNone(result)
        self.assertTrue(any("authentication" in entry.lower() for entry in log.output))

    @patch("audit.auto_pr_generator.Github")
    def test_create_pull_request_handles_unexpected_exception(self, mock_github):
        mock_github.return_value.get_repo.side_effect = Exception("Unexpected error")
        with self.assertLogs(level="ERROR") as log:
            result = auto_pr_generator.create_pull_request(
                github_token="invalid_token",
                repo_name="user/repo"
            )
        self.assertIsNone(result)
        self.assertTrue(any("unexpected error" in entry.lower() for entry in log.output))

if __name__ == "__main__":
    unittest.main()
