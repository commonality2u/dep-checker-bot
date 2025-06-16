# audit/report_generator.py

import json
import logging
import platform
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_environment_metadata():
    """
    Get metadata about the environment (OS, Python version, etc.)
    """
    return {
        "python_version": sys.version,
        "os": platform.system(),
        "os_version": platform.version(),
        "platform": platform.platform()
    }


def calculate_health_score(
        outdated, vulnerabilities, licenses, disallowed_licenses=None
        ):
    """
    Calculate an overall health score (0-100) based on audit results.
    """
    score = 100
    score -= min(len(outdated) * 5, 30)  # up to -30 points
    score -= min(
        sum(len(dep.get("vulnerabilities", [])) for dep in vulnerabilities) * 10, 40
        )  # up to -40 points
    flagged_licenses = [
        pkg for pkg in licenses if pkg.get("license") in (disallowed_licenses or [])
    ]
    score -= min(len(flagged_licenses) * 10, 30)  # up to -30 points

    return max(score, 0)


def generate_markdown_report(report, output_file="audit_report.md"):
    """
    Generate a Markdown version of the audit report.
    """
    lines = [
        f"# Audit Report ({report['report_date']})",
        "",
        f"**Health Score:** {report.get('health_score', 'N/A')}",
        "",
        "## Summary",
        f"- Outdated Dependencies: {report['summary']['outdated_dependencies_count']}",
        f"- Vulnerabilities: {report['summary']['vulnerabilities_count']}",
        f"- Licenses Checked: {report['summary']['licenses_count']}",
        "",
        "## Outdated Dependencies",
    ]
    for dep in report["outdated_dependencies"]:
        lines.append(
            f"- {dep['name']} (current: {dep['current_version']}, latest: {dep['latest_version']})"
            )

    lines.append("\n## Vulnerabilities")
    for vuln in report["vulnerabilities"]:
        lines.append(f"- {vuln['name']} (v{vuln['version']})")
        for v in vuln["vulnerabilities"]:
            lines.append(f"  - **{v['id']}**: {v['description']}")

    lines.append("\n## Licenses")
    for lic in report["licenses"]:
        lines.append(f"- {lic['name']} ({lic['version']}) - License: {lic['license']}")

    lines.append("\n## Environment Metadata")
    metadata = report.get("environment", {})
    for key, value in metadata.items():
        lines.append(f"- **{key}**: {value}")

    try:
        with open(output_file, "w") as f:
            f.write("\n".join(lines))
        logging.info(f"📄 Markdown report saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error saving Markdown report: {e}")


def generate_report(
        outdated_dependencies, 
        vulnerabilities, 
        licenses, 
        disallowed_licenses=None, 
        output_file="audit_report.json", 
        markdown_output_file="audit_report.md"
        ):
    """
    Generate a consolidated audit report in JSON and Markdown formats.

    Parameters:
        outdated_dependencies (list): List of outdated dependencies.
        vulnerabilities (list): List of vulnerabilities.
        licenses (list): List of licenses.
        disallowed_licenses (list): Licenses considered disallowed.
        output_file (str): Path for the JSON report.
        markdown_output_file (str): Path for the Markdown report.

    Returns:
        dict: The consolidated report dictionary.
    """
    health_score = calculate_health_score(
        outdated_dependencies, vulnerabilities, licenses, disallowed_licenses
        )
    environment_metadata = get_environment_metadata()

    report = {
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "outdated_dependencies_count": len(outdated_dependencies),
            "vulnerabilities_count": sum(
                len(dep.get("vulnerabilities", [])) for dep in vulnerabilities
                ),
            "licenses_count": len(licenses),
            "health_score": health_score,
        },
        "health_score": health_score,
        "environment": environment_metadata,
        "outdated_dependencies": outdated_dependencies,
        "vulnerabilities": vulnerabilities,
        "licenses": licenses,
    }

    try:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)
        logging.info(f"✅ Audit report saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error saving audit report: {e}")

    # Also generate Markdown version
    generate_markdown_report(report, markdown_output_file)

    return report


def run():
    """Entry point for CLI execution using sample data."""
    sample_outdated = []
    sample_vulnerabilities = []
    sample_licenses = []
    generate_report(
        sample_outdated,
        sample_vulnerabilities,
        sample_licenses
        )
    
if __name__ == "__main__":
    # Example usage with sample data:
    sample_outdated = [
        {"name": "requests", "current_version": "2.25.0", "latest_version": "2.31.0"}
    ]
    sample_vulnerabilities = [
        {
            "name": "requests",
            "version": "2.25.0",
            "vulnerabilities": [
                {"id": "CVE-1234", "description": "Sample vulnerability"}
            ],
        }
    ]
    sample_licenses = [
        {"name": "requests",
        "version": "2.25.0", 
        "license": "GPL-3.0", 
        "license_text": "GPL License Text",
        }
    ]

    disallowed_licenses = ["GPL-3.0", "AGPL-3.0"]

    generate_report(
        sample_outdated, sample_vulnerabilities, sample_licenses, disallowed_licenses
    )
