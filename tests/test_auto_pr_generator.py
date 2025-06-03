# tests/test_auto_pr_generator.py

import unittest
from unittest.mock import patch, MagicMock
from github import GithubException
from audit import auto_pr_generator

class TestAutoPRGenerator(unittest.TestCase):
    @patch("audit.auto_pr_generator.create_branch_if_not_exists")
    @patch("audit.auto_pr_generator.commit_files_to_branch")
    @patch("audit.auto_pr_generator.Github")
    def test_create_pull_request_success(self, mock_github, mock_commit, mock_branch):
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_pr.html_url = "https://github.com/example/repo/pull/1"
        mock_repo.create_pull.return_value = mock_pr
        mock_github.return_value.get_repo.return_value = mock_repo

        for draft in [True, False]:
            with self.subTest(draft=draft):
                result = auto_pr_generator.create_pull_request(
                    github_token="fake_token",
                    repo_name="user/repo",
                    files_to_commit=["file.txt"],
                    reviewers=["usuario1"],
                    labels=["audit"],
                    draft=draft,
                    min_health_score=None,
                    health_score=70
                )

                self.assertIsNotNone(result)
                mock_repo.create_pull.assert_called()
                args, kwargs = mock_repo.create_pull.call_args
                self.assertEqual(kwargs["draft"], draft)

                # Validar reviewers y labels
                mock_pr.create_review_request.assert_called_with(reviewers=["usuario1"])
                mock_pr.add_to_labels.assert_called_with("audit")

    @patch("audit.auto_pr_generator.Github")
    def test_create_pull_request_with_files_to_commit(self, mock_github):
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_pr.html_url = "https://github.com/example/repo/pull/2"
        mock_repo.create_pull.return_value = mock_pr
        mock_github.return_value.get_repo.return_value = mock_repo

        with patch("audit.auto_pr_generator.commit_files_to_branch") as mock_commit:
            result = auto_pr_generator.create_pull_request(
                github_token="fake_token",
                repo_name="user/repo",
                files_to_commit=["file.txt"],
                health_score=70
            )
            self.assertIsNotNone(result)
            mock_commit.assert_called_once_with(
                mock_repo, "audit/update-dependencies", ["file.txt"], "Audit Report Update", "Audit Bot", "audit@example.com"
            )

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
        mock_github.return_value.get_repo.side_effect = GithubException(401, "Unauthorized", None)
        with self.assertLogs(level="ERROR") as log:
            result = auto_pr_generator.create_pull_request(
                github_token="invalid_token",
                repo_name="user/repo"
            )
        self.assertIsNone(result)
        self.assertTrue(any("authentication failed" in entry.lower() for entry in log.output))
        self.assertTrue(any("ERROR" in entry for entry in log.output))

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
        self.assertTrue(any("ERROR" in entry for entry in log.output))

if __name__ == "__main__":
    unittest.main()
