import subprocess
import json
import logging
import sys
from pathlib import Path


#Basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def check_outdated_dependencies(requirements_file="requirements.txt", use_poetry=False):
    """
    Check for outdated dependencies using pip list --outdated.
    Returns a list of dictionaries with name, installed version, and most recent version.
    """
    dependencies = []
    try:
        if use_poetry:
            logging.info("Checking outdated dependencies using Poetry")
            result = subprocess.run(
                ["poetry", "show", "--outdated", "--format", "json", "--no-dev"],
                capture_output=True, 
                text=True, 
                check=True,
            )
            outdated = json.loads(result.stdout)
            for dep in outdated:
                dependencies.append(
                    {
                    "name": dep["name"],
                    "current_version": dep["installed_version"],
                    "latest_version": dep["latest_version"],
                    }
                )
        else:
            logging.info("Checking outdated dependencies using pip")
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=json"],
                capture_output=True, 
                text=True, 
                check=True,
            )
            outdated = json.loads(result.stdout)
            for dep in outdated:
                dependencies.append(
                    {
                    "name": dep["name"],
                    "current_version": dep["version"],
                    "latest_version": dep["latest_version"]
                    }
                )
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while checking outdated dependencies: {e}")
        return dependencies
    return dependencies

def check_vulnerabilities(requirements_file="requirements.txt", use_poetry=False):  
    """
    Check for vulnerabilities using pip-audit.
    Returns a list of dictionaries with package names and vulnerability details.
    """
    vulnerabilities = []
    try:
        if use_poetry:
            # Export dependencies from Poetry to a requirements file
            export_file = Path("poetry_requirements.txt")
            subprocess.run(
                ["poetry", "export", "-f", "requirements.txt", "-o", str(export_file)],
                capture_output=True, text=True, check=True
            )
            requirements_file = str(export_file)
        
        logging.info("Ejecutando pip-audit para vulnerabilidades...")
        result = subprocess.run(
            ["pip-audit", "--format", "json", "-r", requirements_file],
            capture_output=True, 
            text=True, 
            check=True,
        )
        vulnerabilities_json = json.loads(result.stdout)
        for vuln in vulnerabilities_json:
            vulnerabilities.append(
                {
                "name": vuln["name"],
                "version": vuln["version"],
                "vulnerabilities": [
                    {"id": v["id"], "description": v["description"]}
                    for v in vuln.get("vulns", [])
                ]
                }
            )
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al verificar vulnerabilidades: {e}")
    return vulnerabilities

def main(requirements_file="requirements.txt", use_poetry=False):
    logging.info("=== Analysis of outdated dependencies ===")
    outdated = check_outdated_dependencies(requirements_file, use_poetry=use_poetry)
    for dep in outdated:
        logging.info(
            f"{dep['name']} (actual: {dep['current_version']}, última: {dep['latest_version']})"
        )
    
    logging.info("=== Análisis de vulnerabilidades ===")
    vulnerabilities = check_vulnerabilities(requirements_file, use_poetry)
    for vuln in vulnerabilities:
        logging.info(f"{vuln['name']} (v{vuln['version']})")
        for v in vuln["vulnerabilities"]:
            logging.info(f"  - ID: {v['id']}, Descripción: {v['description']}")
    
    return {"outdated": outdated, "vulnerabilities": vulnerabilities}

def run():
    """Entry point for CLI execution."""
    use_poetry = "--poetry" in sys.argv
    requirements_file = "requirements.txt"
    main(requirements_file, use_poetry)

    
if __name__ == "__main__":
    use_poetry = "--poetry" in sys.argv
    requirements_file = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"
    main(requirements_file, use_poetry)