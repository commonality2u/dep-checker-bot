#!/usr/bin/env python3

import argparse
import sys

# Importar módulos (estos nombres se basan en tu estructura, ajusta si es necesario)
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
    print("[INFO] Ejecutando todas las auditorías...")
    # Aquí puedes llamar a las funciones principales de cada módulo
    # Por ejemplo:
    audit_history.run()
    auto_pr_generator.run()
    badge_generator.run()
    dependency_checker.run()
    license_checker.run()
    nlp_report_summarizer.run()
    policy_loader.run()
    report_generator.run()
    print("[INFO] Todas las auditorías se han ejecutado correctamente.")

def run_module(module_name):
    print(f"[INFO] Ejecutando auditoría: {module_name}")
    # Podrías mapear módulos a funciones principales
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
        print(f"[INFO] Auditoría '{module_name}' ejecutada con éxito.")
    except KeyError:
        print(f"[ERROR] Módulo '{module_name}' no encontrado.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Dep Checker Bot - Herramienta para auditar dependencias y generar reportes."
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Nombre del módulo de auditoría a ejecutar (o 'all' para ejecutarlos todos).",
        default="all"
    )
    args = parser.parse_args()

    if args.module == "all":
        run_all()
    else:
        run_module(args.module)

if __name__ == "__main__":
    main()

