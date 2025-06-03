# tests/test_audit_history.py

import unittest
import json
import io
from unittest.mock import patch, mock_open
from audit import audit_history

class TestAuditHistory(unittest.TestCase):
    @patch("audit.audit_history.open", new_callable=mock_open)
    @patch("audit.audit_history.Path.exists", return_value=True)
    def test_add_audit_entry(self, mock_exists, mock_file):
        # Simular historial previo vacío
        mock_file().read.return_value = "[]"

        report = {
            "report_date": "2025-06-03 10:00:00",
            "health_score": 80,
            "summary": {"outdated_dependencies_count": 2}
        }

        audit_history.add_audit_entry(report, history_file="test_history.json")

        # Validar escritura de archivo JSON
        mock_file.assert_any_call("test_history.json", "w")
        handle = mock_file()
        handle.write.assert_called()
        written_data = "".join(call_arg[0][0] for call_arg in handle.write.call_args_list)

        # Verificar campos obligatorios generados por la función
        for key in ["id", "timestamp", "user", "report_date", "health_score", "summary"]:
            with self.subTest(key=key):
                self.assertIn(f'"{key}"', written_data)

    @patch("audit.audit_history.open", new_callable=mock_open, read_data=json.dumps([
        {"id": "123", "health_score": 85},
        {"id": "456", "health_score": 65}
    ]))
    @patch("audit.audit_history.Path.exists", return_value=True)
    def test_load_audit_history_multiple_entries(self, mock_exists, mock_file):
        history = audit_history.load_audit_history("test_history.json")
        self.assertEqual(len(history), 2)
        scores = [entry["health_score"] for entry in history]
        self.assertIn(85, scores)
        self.assertIn(65, scores)

    @patch("audit.audit_history.open", new_callable=mock_open, read_data=json.dumps([
        {"id": "123", "health_score": 85, "timestamp": "2025-06-03 10:00:00", 
         "report_date": "2025-06-03 09:00:00", "user": "tester", 
         "summary": {"outdated_dependencies_count": 2}}
    ]))
    @patch("audit.audit_history.Path.exists", return_value=True)
    def test_export_audit_history_to_csv(self, mock_exists, mock_file):
        audit_history.export_audit_history_to_csv("test_history.json", "test_history.csv")
        calls = [call[0][0] for call in mock_file.call_args_list]
        self.assertIn("test_history.csv", calls[1])  # Asegura que el CSV se exportó

    @patch("audit.audit_history.open", new_callable=mock_open)
    def test_clear_audit_history(self, mock_file):
        with self.assertLogs(level="INFO") as log:
            audit_history.clear_audit_history("test_history.json")
        mock_file.assert_called_with("test_history.json", "w")
        handle = mock_file()
        handle.write.assert_called()
        written_data = "".join(call_arg[0][0] for call_arg in handle.write.call_args_list)
        self.assertIn("[]", written_data)
        self.assertTrue(any("audit history cleared" in entry.lower() for entry in log.output))

    @patch("audit.audit_history.load_audit_history")
    def test_get_audit_entries_by_score(self, mock_load_history):
        mock_load_history.return_value = [
            {"id": "1", "health_score": 90},
            {"id": "2", "health_score": 50},
            {"id": "3", "health_score": 75}
        ]
        filtered = audit_history.get_audit_entries_by_score(80)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], "1")
    @patch("audit.audit_history.open", new_callable=mock_open, read_data="invalid json")
    @patch("audit.audit_history.Path.exists", return_value=True)
    def test_load_audit_history_invalid_json(self, mock_exists, mock_file):
        with self.assertLogs(level="ERROR") as log:
            history = audit_history.load_audit_history("test_history.json")
        self.assertEqual(history, [])
        self.assertTrue(any("error decoding audit history json" in entry.lower() for entry in log.output))

    @patch("audit.audit_history.open", side_effect=OSError("Permission denied"))
    def test_add_audit_entry_write_error(self, mock_file):
        report = {
            "report_date": "2025-06-03 10:00:00",
            "health_score": 80,
            "summary": {"outdated_dependencies_count": 2}
        }
        with self.assertLogs(level="ERROR") as log:
            audit_history.add_audit_entry(report, history_file="test_history.json")
        self.assertTrue(any("error saving audit history" in entry.lower() for entry in log.output))

    @patch("audit.audit_history.open", side_effect=OSError("Disk full"))
    def test_clear_audit_history_write_error(self, mock_file):
        with self.assertLogs(level="ERROR") as log:
            audit_history.clear_audit_history("test_history.json")
        self.assertTrue(any("error clearing audit history" in entry.lower() for entry in log.output))

    @patch("audit.audit_history.open", new_callable=mock_open, read_data=json.dumps([
        {"id": "123", "health_score": 85, "timestamp": "2025-06-03 10:00:00", 
         "report_date": "2025-06-03 09:00:00", "user": "tester", 
         "summary": {"outdated_dependencies_count": 2}}
    ]))
    @patch("audit.audit_history.Path.exists", return_value=True)
    def test_export_audit_history_to_csv_content(self, mock_exists, mock_file):
        # Simular exportación de CSV usando StringIO
        csv_output = io.StringIO()
        # Forzar open() para devolver StringIO solo en el segundo call (para CSV)
        mock_file.side_effect = [
            mock_open(read_data=json.dumps([
                {"id": "123", "health_score": 85, "timestamp": "2025-06-03 10:00:00",
                "report_date": "2025-06-03 09:00:00", "user": "tester",
                "summary": {"outdated_dependencies_count": 2}}
            ])).return_value, 
            csv_output
        ]
        audit_history.export_audit_history_to_csv("test_history.json", "test_history.csv")
        # Verificar que el CSV tiene los encabezados y contenido esperado
        csv_content = csv_output.getvalue()
        self.assertIn("id", csv_content)
        self.assertIn("health_score", csv_content)
        self.assertIn("123", csv_content)
        header_line = csv_content.splitlines()[0]
        self.assertIn("id", header_line)
        self.assertIn("health_score", header_line)
if __name__ == "__main__":
    unittest.main()
