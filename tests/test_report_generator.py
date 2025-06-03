# tests/test_report_generator.py

import unittest
import json
from unittest.mock import patch, mock_open
from audit import report_generator

class TestReportGenerator(unittest.TestCase):
    @patch("audit.report_generator.open", new_callable=mock_open)
    def test_generate_report(self, mock_file):
        # Datos de prueba
        outdated_dependencies = [
            {"name": "requests", "current_version": "2.25.0", "latest_version": "2.31.0"}
        ]
        vulnerabilities = [
            {
                "name": "requests",
                "version": "2.25.0",
                "vulnerabilities": [
                    {"id": "CVE-1234", "description": "Test vulnerability"}
                ]
            }
        ]
        licenses = [
            {"name": "requests", "version": "2.25.0", "license": "MIT"}
        ]
        disallowed_licenses = ["GPL-3.0", "AGPL-3.0"]

        # Ejecutar la función de reporte
        report = report_generator.generate_report(
            outdated_dependencies, vulnerabilities, licenses, 
            disallowed_licenses, output_file="dummy_report.json", 
            markdown_output_file="dummy_report.md"
        )

        # Validar Health Score (no hay licencias prohibidas => Score 55 o superior)
        self.assertGreaterEqual(report["health_score"], 55)
        self.assertIn("summary", report)
        self.assertEqual(report["summary"]["outdated_dependencies_count"], 1)
        self.assertEqual(report["summary"]["vulnerabilities_count"], 1)
        self.assertEqual(report["summary"]["licenses_count"], 1)

        # Validar metadata de entorno
        for key in ["python_version", "os", "platform"]:
            with self.subTest(key=key):
                self.assertIn(key, report["environment"])

        # Validar que open() se ha llamado 2 veces (JSON + Markdown)
        self.assertEqual(mock_file.call_count, 2)
        opened_files = {call[0][0] for call in mock_file.call_args_list}
        self.assertIn("dummy_report.json", opened_files)
        self.assertIn("dummy_report.md", opened_files)

        # Validar que se escribieron datos en los archivos
        handle = mock_file()
        self.assertTrue(handle.write.called)
        written_content = "".join(call[0][0] for call in handle.write.call_args_list)
        self.assertTrue(len(written_content) > 0)

    def test_calculate_health_score(self):

        # Probar Health Score con dependencias y vulnerabilidades
        outdated = [{"name": "requests"}] * 3
        vulnerabilities = [{"name": "requests", "vulnerabilities": [{"id": "CVE-1234"}]}]
        licenses = [{"name": "requests", "license": "GPL-3.0"}]
        
        # Sin licencias prohibidas
        score = report_generator.calculate_health_score(outdated, vulnerabilities, licenses, disallowed_licenses=["GPL-3.0"])
        self.assertIsInstance(score, int)
        self.assertLessEqual(score, 100)
        self.assertGreaterEqual(score, 0)

    def test_environment_metadata(self):
        metadata = report_generator.get_environment_metadata()
        for key in ["python_version", "os", "platform"]:
            with self.subTest(key=key):
                self.assertIn(key, metadata)

if __name__ == "__main__":
    unittest.main()
