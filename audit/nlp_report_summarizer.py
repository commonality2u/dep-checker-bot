# audit/nlp_report_summarizer.py

import json
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def summarize_report(report_file="audit_report.json"):
    """
    Generate a textual summary from an audit report JSON file.
    """
    path = Path(report_file)
    if not path.exists():
        logging.warning(f"⚠️ Report file not found: {report_file}")
        return "No audit report found."

    try:
        with open(report_file, "r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception as e:
        logging.error(f"Error reading audit report: {e}")
        return "Error reading audit report."

    summary_parts = []
    report_date = report.get("report_date", "Unknown date")
    outdated_count = report.get("summary", {}).get("outdated_dependencies_count", 0)
    vulnerabilities_count = report.get("summary", {}).get("vulnerabilities_count", 0)
    licenses_count = report.get("summary", {}).get("licenses_count", 0)
    health_score = report.get("health_score", "N/A")

    summary_parts.append(f"🔍 Audit performed on {report_date}:")
    summary_parts.append(f"- Outdated dependencies: {outdated_count}")
    summary_parts.append(f"- Vulnerabilities found: {vulnerabilities_count}")
    summary_parts.append(f"- Packages analyzed: {licenses_count}")
    summary_parts.append(f"- Health Score: {health_score}")

    if isinstance(health_score, (int, float)) and health_score < 80:
        summary_parts.append("⚠️ Warning: Health Score is low. Check dependencies and vulnerabilities")
    else:
        summary_parts.append("✅ Health Score is ok.")

    # Add automatic recommendations if there are outdated dependencies
    recommendations = generate_recommendations(report)
    if recommendations:
        summary_parts.append("\n🔧 Recommendations:")
        summary_parts.extend(recommendations)

    # Highlight keywords such as "critical".
    nlp_summary = "\n".join(summary_parts)
    nlp_summary = highlight_keywords(nlp_summary, ["critical", "high", "serious"])

    return nlp_summary


def generate_recommendations(report):
    """
    Generates recommendations based on outdated dependencies.
    """
    recommendations = []
    outdated_deps = report.get("outdated_dependencies", [])
    for dep in outdated_deps:
        name = dep.get("name")
        current_version = dep.get("current_version")
        latest_version = dep.get("latest_version")
        if name and current_version and latest_version:
            recommendations.append(
                f"🔹 Update '{name}' from version {current_version} to {latest_version}."
            )
    return recommendations


def highlight_keywords(text, keywords):
    """
    Highlights specified keywords in the summary.
    """
    for keyword in keywords:
        text = text.replace(keyword, f"**{keyword.upper()}**")
    return text


def run():
    """
    Entry point for the CLI.
    """
    report_file = "audit_report.json"
    summary = summarize_report(report_file)
    print(summary)


if __name__ == "__main__":
    run()