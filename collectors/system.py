import platform
from datetime import datetime,timezone

import psutil

from core.collectors.base import Collector
from core.models.observation import Observation


class SystemCollector(Collector):

        #     That's all for that issue.

        # Why did we change everything to list[Observation]?

        # This is the architectural decision we discussed.

        # System

        # One host:

        # SystemCollector
        #        ↓
        # [ Observation ]
        # Processes

        # Many processes:

        # ProcessCollector
        #        ↓
        # [
        #   Observation,
        #   Observation,
        #   Observation,
        #   Observation,
        #   ...
        # ]

        # So Galaxy now has one universal collector contract:

        # Collector.collect()
        #        ↓
        # list[Observation]

        # Whether the list contains:

        # 1 observation

        # or:

        # 500 observations

        # doesn't matter to the rest of Galaxy.

        # That's exactly what we wanted.

    def collect(self) -> list[Observation]:#
        data = {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": platform.node(),
            "uptime": self._get_uptime(),
        }

        return [Observation(
            source="system",
            entity_type="host",
            entity_id="localhost",
            timestamp=datetime.now(timezone.utc),#datetime.now(),
            data=data,
        )]

    def _get_uptime(self):
        boot_time = psutil.boot_time()
        current_time = datetime.now().timestamp()

        return current_time - boot_time