from datetime import datetime
import os
from typing import List, Optional

import requests

from doctor_canamo.datamodel import Metric
from doctor_canamo.ingestion.base import DataConnector


class GroweeConnector(DataConnector):
    """Minimal Growee client using token-based auth.

    Falls back to synthetic metrics when credentials are not configured.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        device_id: str = "growee-default",
        dry_run: bool = False,
    ):
        self.dry_run = dry_run
        self.base_url = "" if dry_run else base_url or os.getenv("GROWEE_BASE_URL", "")
        self.token = None if dry_run else token or os.getenv("GROWEE_TOKEN")
        self.device_id = device_id

    def fetch_metrics(self) -> List[Metric]:
        if not self.base_url or not self.token:
            return self._synthetic_metrics()

        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/api/v1/metrics", headers=headers, timeout=10)
        response.raise_for_status()
        payload = response.json()
        metrics: List[Metric] = []
        for item in payload.get("data", []):
            metrics.append(
                Metric(
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    source="growee",
                    device_id=item.get("device_id", self.device_id),
                    metric=item["metric"],
                    value=item["value"],
                    unit=item.get("unit"),
                )
            )
        return metrics

    def _synthetic_metrics(self) -> List[Metric]:
        now = datetime.utcnow()
        return [
            Metric(timestamp=now, source="growee", device_id=self.device_id, metric="water_temp", value=20.5, unit="C"),
            Metric(timestamp=now, source="growee", device_id=self.device_id, metric="ec", value=1.6, unit="mS/cm"),
            Metric(timestamp=now, source="growee", device_id=self.device_id, metric="ph", value=5.9, unit="pH"),
        ]
