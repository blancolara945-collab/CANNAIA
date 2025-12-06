from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Metric:
    timestamp: datetime
    source: str
    device_id: str
    metric: str
    value: Any
    unit: Optional[str] = None
    plant_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Diagnosis:
    message: str
    severity: str
    recommendations: List[str]
    metrics_considered: List[Metric]


@dataclass
class DataIssue:
    message: str
    severity: str  # info | warning | error
    metric: Optional[Metric] = None
