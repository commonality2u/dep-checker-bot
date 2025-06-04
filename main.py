#!/usr/bin/env python3

import argparse
import sys
import logging
import importlib
import os
import json

# Default log configuration (will be adjusted according to the --quiet option)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Import modules (make sure they exist)
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

# Module Dictionary
MODULES = {
    "audit_history": audit_history.run,
    "auto_pr_generator": auto_pr_generator.run,
    "badge_generator": badge_generator.run,
    "dependency_checker": dependency_checker.run,
    "license_checker": license_checker.run,
    "nlp_report_summarizer": nlp_report_summarizer.run,
    "policy_loader": policy_loader.run,
    "report_generator": report_generator.run,
}

def run_all(dry_run=False):
    summary = {"success": 0, "failures": 0}
    logging.info("Running all audit modules...")
    for name in MODULES:
        run_module(name, dry_run=dry_run, summary=summary)
    print_summary(summary)
    sys.exit(1 if summary['failures'] > 0 else 0)

def run_module(module_name, dry_run=False, summary=None):
    if module_name not in MODULES:
        logging.error(f"Module '{module_name}' not found.")
        logging.info("Use --list to see available modules.")
        if summary is not None:
            summary['failures'] += 1
        return

    try:
        if dry_run:
            logging.info(f"[Dry-run] Would execute {module_name} ...")
        else:
            logging.info(f"Executing {module_name} ...")
            MODULES[module_name]()
            logging.info(f"Module {module_name} completed successfully.")
        if summary is not None:
            summary['success'] += 1
    except Exception as e:
        logging.error(f"Module {module_name} failed: {e}")
        if summary is not None:
            summary['failures'] += 1

def list_modules():
    print("Available modules:")
    for name in MODULES:
        print(f" - {name}")

def load_config(config_path):
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)
            logging.info(f"Loaded configuration from {config_path}")
            return config
    else:
        logging.error(f"Configuration file {config_path} not found.")
        sys.exit(1)

def print_summary(summary):
    logging.info(f"Execution summary:")
    logging.info(f"  Success: {summary['success']}")
    logging.info(f"  Failures: {summary['failures']}")

def main():
    parser = argparse.ArgumentParser(
        description="Dep Checker Bot - Tool to audit dependencies and generate reports."
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Name of the module(s) to run (comma-separated) or 'all' to run them all."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available audit modules."
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational logs (show only errors)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without actually running the modules."
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to a log file to save the logs."
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to a configuration file (JSON) with modules to run."
    )

    args = parser.parse_args()

    # Log configuration
    log_level = logging.ERROR if args.quiet else logging.INFO
    log_handlers = [logging.StreamHandler(sys.stdout)]
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        log_handlers.append(file_handler)
    logging.basicConfig(level=log_level, format="[%(levelname)s] %(message)s", handlers=log_handlers)

    if args.list:
        list_modules()
        sys.exit(0)

    modules_to_run = []

    if args.config:
        config = load_config(args.config)
        modules_to_run = config.get("modules", [])
    elif args.module:
        if args.module.strip().lower() == "all":
            run_all(dry_run=args.dry_run)
            return
        else:
            modules_to_run = [m.strip() for m in args.module.split(",")]
    else:
        parser.print_help()
        sys.exit(0)

    summary = {"success": 0, "failures": 0}
    for module_name in modules_to_run:
        run_module(module_name, dry_run=args.dry_run, summary=summary)

    print_summary(summary)
    sys.exit(1 if summary['failures'] > 0 else 0)

if __name__ == "__main__":
    main()
