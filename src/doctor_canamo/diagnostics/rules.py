from collections import defaultdict
from typing import Dict, List

from doctor_canamo.datamodel import Diagnosis, Metric

THRESHOLDS = {
    "ph": (5.5, 6.3),
    "ec": (1.2, 2.0),
    "air_temp": (22.0, 28.0),
    "humidity": (45.0, 60.0),
    "water_temp": (18.0, 22.0),
}


def aggregate_by_metric(metrics: List[Metric]) -> Dict[str, List[Metric]]:
    grouped: Dict[str, List[Metric]] = defaultdict(list)
    for metric in metrics:
        grouped[metric.metric].append(metric)
    return grouped


def run_threshold_rules(metrics: List[Metric]) -> List[Diagnosis]:
    grouped = aggregate_by_metric(metrics)
    diagnoses: List[Diagnosis] = []
    for metric_name, points in grouped.items():
        if metric_name not in THRESHOLDS:
            continue
        low, high = THRESHOLDS[metric_name]
        for point in points:
            if point.value < low:
                diagnoses.append(
                    Diagnosis(
                        message=f"{metric_name} por debajo del óptimo ({point.value} < {low})",
                        severity="warning",
                        recommendations=[f"Incrementar {metric_name} hasta {low}"],
                        metrics_considered=[point],
                    )
                )
            elif point.value > high:
                diagnoses.append(
                    Diagnosis(
                        message=f"{metric_name} por encima del óptimo ({point.value} > {high})",
                        severity="warning",
                        recommendations=[f"Reducir {metric_name} hasta {high}"],
                        metrics_considered=[point],
                    )
                )
    return diagnoses
