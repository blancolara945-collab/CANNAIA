from abc import ABC, abstractmethod
from typing import List

from doctor_canamo.datamodel import Metric


class DataConnector(ABC):
    @abstractmethod
    def fetch_metrics(self) -> List[Metric]:
        """Return a list of metrics for this connector."""


class StaticConnector(DataConnector):
    """Connector used for local testing with predefined metrics."""

    def __init__(self, metrics: List[Metric]):
        self.metrics = metrics

    def fetch_metrics(self) -> List[Metric]:
        return self.metrics
