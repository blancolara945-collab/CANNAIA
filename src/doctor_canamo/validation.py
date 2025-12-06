from datetime import datetime, timedelta
from typing import List

from doctor_canamo.datamodel import DataIssue, Metric


STALE_THRESHOLD = timedelta(hours=6)


def validate_metrics(metrics: List[Metric]) -> List[DataIssue]:
    """Run lightweight data-quality checks over collected metrics.

    Checks include:
    - Missing values
    - Stale timestamps (older than STALE_THRESHOLD)
    - Missing units
    """

    issues: List[DataIssue] = []
    now = datetime.utcnow()

    for metric in metrics:
        if metric.value is None:
            issues.append(
                DataIssue(
                    message=f"Valor faltante para {metric.metric} de {metric.source}",
                    severity="error",
                    metric=metric,
                )
            )

        if metric.timestamp and now - metric.timestamp > STALE_THRESHOLD:
            issues.append(
                DataIssue(
                    message=f"Dato desactualizado para {metric.metric} (>{STALE_THRESHOLD} de antigüedad)",
                    severity="warning",
                    metric=metric,
                )
            )

        if metric.unit is None:
            issues.append(
                DataIssue(
                    message=f"Unidad no informada para {metric.metric}",
                    severity="info",
                    metric=metric,
                )
            )

    return issues
