"""Muestra el mismo flujo con la versión inicial o la refactorizada."""

import argparse
from pprint import pprint

from initial.app import AcademicRequestApp
from refactored import create_service
from refactored.models import Category, Priority, RequestDraft


def main():
    parser = argparse.ArgumentParser(description="Demostración del antes y después")
    parser.add_argument("--version", choices=("initial", "refactored"), required=True)
    args = parser.parse_args()

    if args.version == "initial":
        system = AcademicRequestApp()
        first = system.register(1, "certificate", "high", "Constancia de alumno")
        system.register(2, "schedule", "low", "Consulta de horario")
    else:
        system = create_service()
        first = system.register(RequestDraft(1, Category.CERTIFICATE, Priority.HIGH, "Constancia de alumno"))
        system.register(RequestDraft(2, Category.SCHEDULE, Priority.LOW, "Consulta de horario"))

    system.assign_area(first["id"], 1)
    system.change_status(first["id"], "in_progress")
    print("Solicitudes:")
    pprint(system.list_requests())
    print("Reporte:")
    pprint(system.report())


if __name__ == "__main__":
    main()
