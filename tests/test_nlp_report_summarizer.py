# tests/test_nlp_report_summarizer.py

import unittest
import json
from unittest.mock import patch, mock_open
from audit import nlp_report_summarizer

class TestNLPReportSummarizer(unittest.TestCase):
    @patch("audit.nlp_report_summarizer.Path.exists", return_value=True)
    @patch("audit.nlp_report_summarizer.open", new_callable=mock_open, read_data=json.dumps({
        "report_date": "2025-06-03",
        "summary": {
            "outdated_dependencies_count": 2,
            "vulnerabilities_count": 1,
            "licenses_count": 10
        },
        "health_score": 75,
        "outdated_dependencies": [
            {"name": "requests", "current_version": "2.25.0", "latest_version": "2.31.0"}
        ]
    }))
    def test_summarize_report_success(self, mock_open_file, mock_exists):
        summary = nlp_report_summarizer.summarize_report("audit_report.json")
        self.assertIn("🔍 Audit performed on 2025-06-03:", summary)
        self.assertIn("Outdated dependencies: 2", summary)
        self.assertIn("Vulnerabilities found: 1", summary)
        self.assertIn("Health Score: 75", summary)
        self.assertIn("⚠️ Warning", summary)
        self.assertIn("Update 'requests' from version 2.25.0 to 2.31.0", summary)

    @patch("audit.nlp_report_summarizer.Path.exists", return_value=False)
    def test_summarize_report_file_not_found(self, mock_exists):
        summary = nlp_report_summarizer.summarize_report("audit_report.json")
        self.assertIn("No audit report found", summary)

    @patch("audit.nlp_report_summarizer.Path.exists", return_value=True)
    @patch("audit.nlp_report_summarizer.open", new_callable=mock_open, read_data="invalid json")
    def test_summarize_report_invalid_json(self, mock_open_file, mock_exists):
        summary = nlp_report_summarizer.summarize_report("audit_report.json")
        self.assertIn("Error reading audit report", summary)

    def test_generate_recommendations(self):
        report = {
            "outdated_dependencies": [
                {"name": "flask", "current_version": "1.1.0", "latest_version": "2.0.0"}
            ]
        }
        recommendations = nlp_report_summarizer.generate_recommendations(report)
        self.assertEqual(len(recommendations), 1)
        self.assertIn("flask", recommendations[0])
        self.assertIn("1.1.0", recommendations[0])
        self.assertIn("2.0.0", recommendations[0])

    def test_highlight_keywords(self):
        text = "This is a critical and high severity vulnerability."
        highlighted = nlp_report_summarizer.highlight_keywords(text, ["critical", "high"])
        self.assertIn("**CRITICAL**", highlighted)
        self.assertIn("**HIGH**", highlighted)

if __name__ == "__main__":
    unittest.main()
