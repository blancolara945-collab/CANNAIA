import logging
from pathlib import Path
from typing import Iterable, List

from doctor_canamo.automation.actions import Action, plan_actions
from doctor_canamo.datamodel import DataIssue, Diagnosis, Metric
from doctor_canamo.diagnostics.rules import run_threshold_rules
from doctor_canamo.storage.excel_writer import ExcelWriter
from doctor_canamo.validation import validate_metrics

logger = logging.getLogger(__name__)


def collect_metrics(connectors: Iterable) -> List[Metric]:
    metrics: List[Metric] = []
    for connector in connectors:
        connector_name = connector.__class__.__name__
        logger.debug("Invocando conector %s", connector_name)
        new_metrics = connector.fetch_metrics()
        logger.debug("%s devolvió %d métricas", connector_name, len(new_metrics))
        metrics.extend(new_metrics)
    return metrics


def diagnose(metrics: List[Metric]) -> List[Diagnosis]:
    return run_threshold_rules(metrics)


def orchestrate(
    output_excel: Path, connectors: Iterable
) -> tuple[list[Metric], list[Diagnosis], list[Action], list[DataIssue]]:
    connectors = list(connectors)
    logger.info("Iniciando orquestación: %d conectores", len(connectors))

    metrics = collect_metrics(connectors)
    logger.info("Métricas recopiladas: %d", len(metrics))

    data_issues = validate_metrics(metrics)
    logger.info("Alertas de calidad de datos: %d", len(data_issues))

    diagnoses = diagnose(metrics)
    logger.info("Diagnósticos generados: %d", len(diagnoses))

    actions = plan_actions(diagnoses)
    logger.info("Acciones propuestas: %d", len(actions))

    writer = ExcelWriter(output_excel)
    writer.write_metrics(metrics)
    writer.append_diagnoses(diagnoses)
    writer.append_data_issues(data_issues)
    writer.append_actions(actions)

    return metrics, diagnoses, actions, data_issues
