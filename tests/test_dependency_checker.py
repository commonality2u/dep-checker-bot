# test_dependency_checker.py

import unittest
import json
from unittest.mock import patch
from audit import dependency_checker

class TestDependencyChecker(unittest.TestCase):
    @patch('audit.dependency_checker.subprocess.run')
    def test_check_outdated_dependencies_pip(self, mock_run):
        mock_run.return_value.stdout = json.dumps([
            {"name": "requests", "version": "2.25.0", "latest_version": "2.31.0"}
        ])
        mock_run.return_value.returncode = 0
        result = dependency_checker.check_outdated_dependencies()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "requests")
        self.assertEqual(result[0]['current_version'], "2.25.0")
        self.assertEqual(result[0]['latest_version'], "2.31.0")

    @patch('audit.dependency_checker.subprocess.run')
    def test_check_vulnerabilities_pip_audit(self, mock_run):
        mock_run.return_value.stdout = json.dumps([
            {"name": "requests", "version": "2.25.0", "vulns": [{"id": "CVE-1234", "description": "Test vuln"}]}
        ])
        mock_run.return_value.returncode = 0
        result = dependency_checker.check_vulnerabilities()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "requests")
        self.assertEqual(result[0]['version'], "2.25.0")
        self.assertEqual(result[0]['vulnerabilities'][0]['id'], "CVE-1234")

if __name__ == '__main__':
    unittest.main()
