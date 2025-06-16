# audit/license_checker.py

import subprocess
import json
import logging
from pathlib import Path

DISALLOWED_LICENSES = ["GPL-3.0", "AGPL-3.0"]

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
def export_poetry_requirements():
    """
    Export dependencies from Poetry to requirements.txt.
    This function is used to ensure that the dependencies are in a format
    compatible with pip-licenses.
    """
    export_file = Path("poetry_requirements.txt")
    subprocess.run(
        ["poetry", "export", "-f", "requirements.txt", "-o", str(export_file)],
        capture_output=True, text=True, check=True
    )
    return str(export_file)


def check_disallowed_licenses(licenses, disallowed=DISALLOWED_LICENSES):
    flagged = [pkg for pkg in licenses if pkg["license"] in disallowed]
    if flagged:
        logging.warning("⚠️ Licenses not allowed found:")
        for pkg in flagged:
            logging.warning(f"- {pkg['name']} ({pkg['license']})")
    return flagged

#Export licenses to a JSON file
def export_licenses_to_json(licenses, output_file = "licenses.json"):
    """Export the licenses list to a JSON file."""
    with open (output_file, "w") as f:
        json.dump(licenses, f, indent =4)
    logging.info(f"Licneses report saved to: {output_file}")
    
def check_licenses(requirements_file="requirements.txt", use_poetry=False, output_file="licenses.json"):
    """
    Check for license compliance using pip-licenses (or liccheck).
    
    
    Note:
        - pip-licenses analiza las dependencias actualmente instaladas
          en el entorno virtual y no usa directamente el archivo requirements.txt.
          El argumento requirements_file se mantiene para consistencia con el resto
          del proyecto y por si se quiere usar liccheck u otra herramienta en el futuro.
    
    Parameters:
        requirements_file (str): Ruta del archivo de requisitos (no se usa directamente).
        use_poetry (bool): Si es True, exporta dependencias desde Poetry.
        output_file (str): Ruta de exportación para el reporte JSON.
    
    Returns:
        list: Lista de paquetes con información de licencias.
    """
    licenses = []
    try:
        # Export requirements.txt from Poetry if needed
        if use_poetry:
            logging.info("Exporting dependencies from Poetry...")
            requirements_file = export_poetry_requirements()
        
        logging.info("Checking licenses using pip-licenses...")
        result = subprocess.run(
            ["pip-licenses", "--format", "json", "--from=mixed"],
            capture_output=True, text=True, check=True
        )
        licenses_json = json.loads(result.stdout)
        for lic in licenses_json:
            licenses.append({
                "name": lic.get("Name"),
                "version": lic.get("Version"),
                "license": lic.get("License"),
                "license_text": lic.get("LicenseText", "N/A")
            })

        # Check for disallowed licenses
        export_licenses_to_json(licenses, output_file)
        check_disallowed_licenses(licenses)
    except FileNotFoundError as e:
        logging.error(f"Error: {e}. Ensure pip-licenses is installed.")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON output: {e}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while checking licenses: {e}")

    return licenses

def main(requirements_file="requirements.txt", use_poetry=False):
    licenses = check_licenses(requirements_file, use_poetry)
    logging.info("=== License analysis ===")
    for lic in licenses:
        logging.info(f"{lic['name']} (v{lic['version']}) - License: {lic['license']}")
    return licenses

if __name__ == "__main__":
    import sys
    use_poetry = "--poetry" in sys.argv
    requirements_file = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"
    main(requirements_file, use_poetry)
