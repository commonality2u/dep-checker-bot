# audit/audit_history.py

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
import csv
import getpass

HISTORY_FILE = "audit_history.json"

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def add_audit_entry(report, history_file=HISTORY_FILE):
    """
    Add an audit report entry to the audit history file.
    """
    history = []
    history_path = Path(history_file)

    if history_path.exists():
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError as e:
            logging.warning(f"⚠️ Could not load audit history (invalid JSON): {e}. Starting a new history.")
        except Exception as e:
            logging.warning(f"⚠️ Could not load audit history: {e}. Starting a new history.")

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": getpass.getuser(),
        "report_date": report.get("report_date"),
        "health_score": report.get("health_score"),
        "summary": report.get("summary", {}),
    }
    history.append(entry)

    try:
        with open(history_file, "w") as f:
            json.dump(history, f, indent=4)
        logging.info(f"✅ Audit entry added to history: {history_file}")
    except Exception as e:
        logging.error(f"Error saving audit history: {e}")

def load_audit_history(history_file=HISTORY_FILE):
    """
    Load the audit history from the JSON file.
    """
    history_path = Path(history_file)
    if not history_path.exists():
        logging.warning(f"⚠️ Audit history file not found: {history_file}. Returning empty history.")
        return []

    try:
        with open(history_file, "r") as f:
            history = json.load(f)
        return history
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding audit history JSON: {e}")
    except Exception as e:
        logging.error(f"Error loading audit history: {e}")
    return []

def export_audit_history_to_csv(history_file=HISTORY_FILE, csv_file="audit_history.csv"):
    """
    Export the audit history to a CSV file.
    """
    history = load_audit_history(history_file)
    if not history:
        logging.warning("⚠️ No audit history to export.")
        return

    keys = history[0].keys()
    try:
        f = open(csv_file, "w", newline="")
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(history)
        f.flush()
        logging.info(f"✅ Audit history e)xported to: {csv_file}")
    except Exception as e:
        logging.error(f"Error exporting audit history to CSV: {e}")

def clear_audit_history(history_file=HISTORY_FILE):
    """
    Clear the audit history file.
    """
    try:
        with open(history_file, "w") as f:
            json.dump([], f, indent=4)
        logging.info(f"✅ Audit history cleared: {history_file}")
    except Exception as e:
        logging.error(f"Error clearing audit history: {e}")

def get_audit_entries_by_score(min_score, history_file=HISTORY_FILE):
    """
    Get audit entries with health score >= min_score.
    """
    history = load_audit_history(history_file)
    filtered = [entry for entry in history if entry.get("health_score", 0) >= min_score]
    return filtered

def run():
    """Simple demostration run for the CLI."""
    history = load_audit_history()
    print(json.dumps(history, indent=4))
    export_audit_history_to_csv()

if __name__ == "__main__":
    run()