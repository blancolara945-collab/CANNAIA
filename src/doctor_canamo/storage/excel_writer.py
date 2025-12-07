from pathlib import Path
from typing import Iterable, List

import pandas as pd

from doctor_canamo.datamodel import DataIssue, Diagnosis, Metric


class ExcelWriter:
    def __init__(self, output_path: Path):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def write_metrics(self, metrics: Iterable[Metric]) -> Path:
        rows = [
            {
                "timestamp": m.timestamp.isoformat(),
                "source": m.source,
                "device_id": m.device_id,
                "metric": m.metric,
                "value": m.value,
                "unit": m.unit,
                "plant_id": m.plant_id,
            }
            for m in metrics
        ]
        df = pd.DataFrame(rows)
        with pd.ExcelWriter(self.output_path, mode="w", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="metrics", index=False)
        return self.output_path

    def append_diagnoses(self, diagnoses: List[Diagnosis]) -> Path:
        self._ensure_metrics_sheet()

        diag_rows = [
            {
                "timestamp": d.metrics_considered[0].timestamp.isoformat() if d.metrics_considered else None,
                "severity": d.severity,
                "message": d.message,
                "recommendations": " | ".join(d.recommendations),
            }
            for d in diagnoses
        ]
        diag_df = pd.DataFrame(diag_rows)
        with pd.ExcelWriter(self.output_path, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            existing_metrics = pd.read_excel(self.output_path, sheet_name="metrics")
            existing_metrics.to_excel(writer, sheet_name="metrics", index=False)
            diag_df.to_excel(writer, sheet_name="diagnoses", index=False)
        return self.output_path

    def append_data_issues(self, issues: List[DataIssue]) -> Path:
        self._ensure_metrics_sheet()

        issue_rows = [
            {
                "timestamp": issue.metric.timestamp.isoformat() if issue.metric else None,
                "source": issue.metric.source if issue.metric else None,
                "metric": issue.metric.metric if issue.metric else None,
                "severity": issue.severity,
                "message": issue.message,
            }
            for issue in issues
        ]
        issues_df = pd.DataFrame(issue_rows)
        with pd.ExcelWriter(self.output_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            issues_df.to_excel(writer, sheet_name="data_quality", index=False)
        return self.output_path

    def append_actions(self, actions: List) -> Path:
        self._ensure_metrics_sheet()

        action_rows = [
            {
                "target": action.target,
                "command": action.command,
                "value": action.value,
                "unit": action.unit,
                "rationale": action.rationale,
            }
            for action in actions
        ]
        actions_df = pd.DataFrame(action_rows)
        with pd.ExcelWriter(self.output_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            actions_df.to_excel(writer, sheet_name="actions", index=False)
        return self.output_path

    def _ensure_metrics_sheet(self) -> None:
        if not self.output_path.exists():
            raise FileNotFoundError(f"Metrics file not found: {self.output_path}")
