from datetime import datetime
import os
from typing import List, Optional

from doctor_canamo.datamodel import Metric
from doctor_canamo.ingestion.base import DataConnector


class DriveConnector(DataConnector):
    """Collects image references stored in a Drive folder.

    The connector only tracks metadata; actual download should be handled separately.
    """

    def __init__(self, folder_path: Optional[str] = None, device_id: str = "drive-folder"):
        self.folder_path = folder_path or os.getenv("DRIVE_FOLDER", "")
        self.device_id = device_id

    def fetch_metrics(self) -> List[Metric]:
        if not self.folder_path:
            return []

        # For now we emit simple metadata using file timestamps.
        metrics: List[Metric] = []
        for filename in sorted(os.listdir(self.folder_path)):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            filepath = os.path.join(self.folder_path, filename)
            stat = os.stat(filepath)
            timestamp = datetime.fromtimestamp(stat.st_mtime)
            metrics.append(
                Metric(
                    timestamp=timestamp,
                    source="drive",
                    device_id=self.device_id,
                    metric="image_ref",
                    value=filepath,
                    unit="path",
                )
            )
        return metrics
