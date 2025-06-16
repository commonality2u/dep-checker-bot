# audit/__init__.py

"""
Audit package for dependency and security auditing.

Modules included:
- dependency_checker: Detect outdated dependencies and vulnerabilities.
- license_checker: Check license compliance of dependencies.
- report_generator: Generate consolidated JSON and Markdown reports.
- audit_history: Manage audit history records.
- auto_pr_generator: Automatically generate GitHub Pull Requests.
- nlp_report_summarizer: Summarize audit reports using NLP.
"""

__version__ = "1.0.0"

__all__ = [
    "dependency_checker",
    "license_checker",
    "report_generator",
    "audit_history",
    "auto_pr_generator",
    "nlp_report_summarizer",
]
def get_version():
    """
    Get the current version of the audit package.
    
    Returns:
        str: The version string.
    """
    return __version__