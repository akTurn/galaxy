import subprocess

from datetime import datetime, timezone

from core.collectors.base import Collector
from core.models.observation import Observation


class ServiceCollector(Collector):

    def collect(self) -> list[Observation]:

        observations = []

        # --------------------------------------------------
        # Get all service units and their states
        # --------------------------------------------------

        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--all",
                "--no-legend",
                "--no-pager",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        # --------------------------------------------------
        # Get MainPID for all services in one call
        # --------------------------------------------------

        main_pids = self._get_main_pids()

        now = datetime.now(timezone.utc)

        # --------------------------------------------------
        # Create observations
        # --------------------------------------------------

        for line in result.stdout.splitlines():

            parts = line.split(None, 4)

            if len(parts) < 4:
                continue

            unit = parts[0]
            load_state = parts[1]
            active_state = parts[2]
            sub_state = parts[3]

            if not unit.endswith(".service"):
                continue

            service_name = unit[:-8]

            main_pid = main_pids.get(unit)

            observations.append(
                Observation(
                    source="systemd",
                    entity_type="service",
                    entity_id=service_name,
                    timestamp=now,
                    # data={
                    #     "name": service_name,
                    #     "unit": unit,
                    #     "load_state": load_state,
                    #     "active_state": active_state,
                    #     "sub_state": sub_state,
                    #     "main_pid": main_pid,
                    # },

                    data={
                        "identity": {
                            "name": service_name,
                            "unit": unit,
                        },
                        "state": {
                            "load": load_state,
                            "active": active_state,
                            "sub": sub_state,
                        },
                        "runtime": {
                            "main_pid": main_pid,
                        },
                    }
                )
            )

        return observations

    def _get_main_pids(self) -> dict[str, int | None]:

        """
        Fetch MainPID for all systemd services in one subprocess call.

        Returns:

            {
                "cron.service": 123,
                "ssh.service": 456,
                "postgresql.service": 789,
            }

        MainPID=0 means the service currently has no running
        main process, so it is represented as None.
        """

        result = subprocess.run(
            [
                "systemctl",
                "show",
                "--type=service",
                "--property=Id,MainPID",
                "--no-pager",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        main_pids = {}

        current_unit = None

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("Id="):

                current_unit = line[3:]

            elif line.startswith("MainPID="):

                if current_unit is None:
                    continue

                value = line[8:]

                try:
                    pid = int(value)
                except ValueError:
                    pid = None

                if pid == 0:
                    pid = None

                main_pids[current_unit] = pid

                current_unit = None

        return main_pids