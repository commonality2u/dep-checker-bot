# audit/policy_loader.py

import json
import logging
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DEFAULT_POLICY = {
    "licenses": {
        "disallowed": []
    },
    "dependencies": {
        "minimum_versions": {}
    }
}


def load_policy(file_path="license_policy.json"):
    """
    Load audit policy from a JSON or YAML file.
    """
    policy_file = Path(file_path)
    policy = {}

    if not policy_file.exists():
        logging.warning(f"⚠️ Policy file not found: {file_path}. Using default policy.")
        policy = DEFAULT_POLICY.copy()
    else:
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as f:
                    policy = json.load(f)
            elif file_path.endswith((".yml", ".yaml")):
                if yaml is None:
                    logging.error("⚠️ YAML support not available. Install PyYAML to enable it.")
                    policy = DEFAULT_POLICY.copy()
                else:
                    with open(file_path, "r") as f:
                        policy = yaml.safe_load(f)
            else:
                logging.error(f"Unsupported policy file format: {file_path}. Using default policy.")
                policy = DEFAULT_POLICY.copy()
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON policy: {e}. Using default policy.")
            policy = DEFAULT_POLICY.copy()
        except Exception as e:
            logging.error(f"Error loading policy file: {e}. Using default policy.")
            policy = DEFAULT_POLICY.copy()

    validate_policy_structure(policy)
    logging.info(f"✅ Policy loaded from: {file_path if policy_file.exists() else 'default'}")
    return policy


def validate_policy_structure(policy):
    """
    Validate the structure of the policy file.
    Logs warnings if expected keys are missing.
    """
    if "licenses" not in policy:
        logging.warning("⚠️ Policy missing 'licenses' section. Adding default.")
        policy["licenses"] = {"disallowed": []}
    else:
        if "disallowed" not in policy["licenses"]:
            logging.warning("⚠️ Policy missing 'licenses.disallowed'. Adding default.")
            policy["licenses"]["disallowed"] = []

    if "dependencies" not in policy:
        logging.warning("⚠️ Policy missing 'dependencies' section. Adding default.")
        policy["dependencies"] = {"minimum_versions": {}}
    else:
        if "minimum_versions" not in policy["dependencies"]:
            logging.warning("⚠️ Policy missing 'dependencies.minimum_versions'. Adding default.")
            policy["dependencies"]["minimum_versions"] = {}


def run():
    """Entry point for the CLI."""
    policy = load_policy("license_policy.json")
    print(json.dumps(policy, indent=4))


if __name__ == "__main__":
    run()
