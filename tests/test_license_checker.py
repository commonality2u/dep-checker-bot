# tests/test_license_checker.py

import unittest
import json
from unittest.mock import patch, mock_open
from audit import license_checker

class TestLicenseChecker(unittest.TestCase):
    @patch('audit.license_checker.open', new_callable=mock_open)
    @patch('audit.license_checker.subprocess.run')
    def test_check_licenses(self, mock_run, mock_file):
        mock_run.return_value.stdout = json.dumps([
            {"Name": "requests", "Version": "2.25.0", "License": "MIT", "LicenseText": "MIT License Text"}
        ])
        mock_run.return_value.returncode = 0

        result = license_checker.check_licenses()
        #Check result structure
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "requests")
        self.assertEqual(result[0]['version'], "2.25.0")
        self.assertEqual(result[0]['license'], "MIT")
        self.assertEqual(result[0]['license_text'], "MIT License Text")

        #Check exported JSON file
        mock_file.assert_called_with('licenses.json', 'w')
        handle = mock_file()
        handle.write.assert_called() #Check if write was called

        #Check called subprocess command
        mock_run.assert_called_with(
            ["pip-licenses", "--format", "json", "--from=mixed"],
            capture_output=True, text=True, check=True
        )
    @patch('audit.license_checker.subprocess.run')
    def test_check_disallowed_licenses(self, mock_run):
        mock_run.return_value.stdout = json.dumps([
            {"Name": "django", "Version": "3.0.0", "License": "GPL-3.0", "LicenseText": "GPL License Text"}
        ])
        mock_run.return_value.returncode = 0

        with self.assertLogs(level = 'WARNING') as log:
            result = license_checker.check_licenses()
        self.assertIn("⚠️ Licenses not allowed found:", "".join(log.output))
        self.assertTrue(any("django" in entry for entry in log.output))
        
if __name__ == '__main__':
    unittest.main()
