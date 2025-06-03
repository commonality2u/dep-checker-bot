#!/usr/bin/env python3

import argparse
import sys

#Import modules (these names are based on your structure, adjust if necessary)
from audit import (
    audit_history,
    auto_pr_generator,
    badge_generator,
    dependency_checker,
    license_checker,
    nlp_report_summarizer,
    policy_loader,
    report_generator,
)

def run_all():
    print("[INFO] Running all audits ...")
    # Here you can call the main functions of each module
    audit_history.run()
    auto_pr_generator.run()
    badge_generator.run()
    dependency_checker.run()
    license_checker.run()
    nlp_report_summarizer.run()
    policy_loader.run()
    report_generator.run()
    print("[INFO] All audits have been executed correctly.")

def run_module(module_name):
    print(f"[INFO] Running audit: {module_name}")
    # You could map modules to main functions
    module_map = {
        "audit_history": audit_history.run,
        "auto_pr_generator": auto_pr_generator.run,
        "badge_generator": badge_generator.run,
        "dependency_checker": dependency_checker.run,
        "license_checker": license_checker.run,
        "nlp_report_summarizer": nlp_report_summarizer.run,
        "policy_loader": policy_loader.run,
        "report_generator": report_generator.run,
    }
    try:
        module_map[module_name]()
        print(f"[INFO] Audit '{module_name}' successfully executed.")
    except KeyError:
        print(f"[ERROR] Module '{module_name}' not found.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Dep Checker Bot - Tool to audit dependencies and generate reports."
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Name of the audit module to run (or 'all' to run them all).",
        default="all"
    )
    args = parser.parse_args()

    if args.module == "all":
        run_all()
    else:
        run_module(args.module)

if __name__ == "__main__":
    main()

