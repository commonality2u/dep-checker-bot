# tests/test_policy_loader.py

import unittest
import json
from unittest.mock import patch, mock_open
from audit import policy_loader

class TestPolicyLoader(unittest.TestCase):
    @patch("audit.policy_loader.open", new_callable=mock_open, read_data=json.dumps({
        "licenses": {"disallowed": ["GPL-3.0"]},
        "dependencies": {"minimum_versions": {"requests": "2.25.0"}}
    }))
    @patch("audit.policy_loader.Path.exists", return_value=True)
    def test_load_policy_json_valid(self, mock_exists, mock_file):
        policy = policy_loader.load_policy("license_policy.json")
        self.assertIn("licenses", policy)
        self.assertIn("disallowed", policy["licenses"])
        self.assertEqual(policy["licenses"]["disallowed"], ["GPL-3.0"])
        self.assertIn("dependencies", policy)
        self.assertIn("minimum_versions", policy["dependencies"])
        self.assertEqual(policy["dependencies"]["minimum_versions"]["requests"], "2.25.0")

    @patch("audit.policy_loader.open", new_callable=mock_open, read_data="invalid json")
    @patch("audit.policy_loader.Path.exists", return_value=True)
    def test_load_policy_json_invalid(self, mock_exists, mock_file):
        with self.assertLogs(level="ERROR") as log:
            policy = policy_loader.load_policy("license_policy.json")
        self.assertEqual(policy, policy_loader.DEFAULT_POLICY)
        self.assertTrue(any("error decoding json" in entry.lower() for entry in log.output))

    @patch("audit.policy_loader.Path.exists", return_value=False)
    def test_load_policy_file_not_found(self, mock_exists):
        with self.assertLogs(level="WARNING") as log:
            policy = policy_loader.load_policy("nonexistent.json")
        self.assertEqual(policy, policy_loader.DEFAULT_POLICY)
        self.assertTrue(any("policy file not found" in entry.lower() for entry in log.output))

    def test_validate_policy_structure_missing_keys(self):
        # Incomplete policy
        incomplete_policy = {}
        with self.assertLogs(level="WARNING") as log:
            policy_loader.validate_policy_structure(incomplete_policy)
        self.assertIn("licenses", incomplete_policy)
        self.assertIn("disallowed", incomplete_policy["licenses"])
        self.assertIn("dependencies", incomplete_policy)
        self.assertIn("minimum_versions", incomplete_policy["dependencies"])
        self.assertTrue(any("missing" in entry.lower() for entry in log.output))

if __name__ == "__main__":
    unittest.main()
