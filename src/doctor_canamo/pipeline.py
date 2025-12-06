from pathlib import Path
from typing import Iterable, List

from doctor_canamo.automation.actions import Action, plan_actions
from doctor_canamo.datamodel import DataIssue, Diagnosis, Metric
from doctor_canamo.diagnostics.rules import run_threshold_rules
from doctor_canamo.storage.excel_writer import ExcelWriter
from doctor_canamo.validation import validate_metrics


def collect_metrics(connectors: Iterable) -> List[Metric]:
    metrics: List[Metric] = []
    for connector in connectors:
        metrics.extend(connector.fetch_metrics())
    return metrics


def diagnose(metrics: List[Metric]) -> List[Diagnosis]:
    return run_threshold_rules(metrics)


def orchestrate(
    output_excel: Path, connectors: Iterable
) -> tuple[list[Metric], list[Diagnosis], list[Action], list[DataIssue]]:
    metrics = collect_metrics(connectors)
    data_issues = validate_metrics(metrics)
    diagnoses = diagnose(metrics)
    actions = plan_actions(diagnoses)

    writer = ExcelWriter(output_excel)
    writer.write_metrics(metrics)
    writer.append_diagnoses(diagnoses)
    writer.append_data_issues(data_issues)
    writer.append_actions(actions)

    return metrics, diagnoses, actions, data_issues
