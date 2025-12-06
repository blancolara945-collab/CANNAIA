from datetime import datetime
import os
from typing import List, Optional

import requests

from doctor_canamo.datamodel import Metric
from doctor_canamo.ingestion.base import DataConnector


class SmartLifeConnector(DataConnector):
    """Tuya/SmartLife connector (polling the cloud REST API).

    Falls back to synthetic metrics when credentials are missing.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        access_token: Optional[str] = None,
        device_id: str = "smartlife-default",
        dry_run: bool = False,
    ):
        self.dry_run = dry_run
        self.api_url = "" if dry_run else api_url or os.getenv("SMARTLIFE_API_URL", "")
        self.access_token = None if dry_run else access_token or os.getenv("SMARTLIFE_ACCESS_TOKEN")
        self.device_id = device_id

    def fetch_metrics(self) -> List[Metric]:
        if not self.api_url or not self.access_token:
            return self._synthetic_metrics()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.api_url}/devices/{self.device_id}/status", headers=headers, timeout=10)
        response.raise_for_status()
        payload = response.json()
        now = datetime.utcnow()
        metrics = [
            Metric(timestamp=now, source="smartlife", device_id=self.device_id, metric="air_temp", value=payload["temperature"], unit="C"),
            Metric(timestamp=now, source="smartlife", device_id=self.device_id, metric="humidity", value=payload["humidity"], unit="%"),
        ]
        return metrics

    def _synthetic_metrics(self) -> List[Metric]:
        now = datetime.utcnow()
        return [
            Metric(timestamp=now, source="smartlife", device_id=self.device_id, metric="air_temp", value=25.0, unit="C"),
            Metric(timestamp=now, source="smartlife", device_id=self.device_id, metric="humidity", value=55.0, unit="%"),
        ]
