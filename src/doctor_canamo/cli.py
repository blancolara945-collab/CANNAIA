import argparse
import logging
from pathlib import Path
from pprint import pprint

from doctor_canamo.ingestion.growee import GroweeConnector
from doctor_canamo.ingestion.smartlife import SmartLifeConnector
from doctor_canamo.ingestion.drive import DriveConnector
from doctor_canamo.pipeline import orchestrate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta el pipeline de Doctor Cañamo")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/doctor_canamo.xlsx"),
        help="Ruta del Excel a generar",
    )
    parser.add_argument(
        "--drive-folder",
        type=Path,
        default=None,
        help="Carpeta local con fotos sincronizadas desde Drive",
    )
    parser.add_argument("--dry-run", action="store_true", help="Usar métricas sintéticas en lugar de llamar a APIs")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Nivel de log para depuración (ej. DEBUG para más detalle)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

    growee_connector = GroweeConnector(dry_run=args.dry_run)
    smartlife_connector = SmartLifeConnector(dry_run=args.dry_run)
    drive_connector = DriveConnector(folder_path=str(args.drive_folder) if args.drive_folder else None)

    metrics, diagnoses, actions, data_issues = orchestrate(
        output_excel=args.output,
        connectors=[growee_connector, smartlife_connector, drive_connector],
    )

    print(f"Excel generado en: {args.output}")
    print("\nDiagnósticos:")
    pprint(diagnoses)
    print("\nAcciones propuestas:")
    pprint(actions)
    print("\nAlertas de calidad de datos:")
    pprint(data_issues)


if __name__ == "__main__":
    main()
