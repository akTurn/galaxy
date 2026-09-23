import json
import subprocess
import hashlib

from datetime import datetime, timezone

from core.collectors.base import Collector
from core.models.observation import Observation


class LogCollector(Collector):


    # Why last_cursor belongs to the collector

    # The collector now has a tiny amount of state:

    # LogCollector
    #     │
    #     └── last_cursor

    # Initially:

    # last_cursor = None

    # After the first collection:

    # last_cursor = "s=...;i=..."

    # On the next collection, that cursor is passed to journalctl.
    
    def __init__(self):
        self.last_cursor = None

    def collect(self) -> list[Observation]:

        # result = subprocess.run(
        #     [
        #         "journalctl",
        #         "-n",
        #         "100",
        #         "--no-pager",
        #         "-o",
        #         "json",
        #     ],
        #     capture_output=True,
        #     text=True,
        #     check=False,
        # )

        command = [
            "journalctl",
            "--no-pager",
            "-o",
            "json",
        ]

        if self.last_cursor is None:
            command.extend([
                "-n",
                "100",
            ])
        else:
            command.extend([
                "--after-cursor",
                self.last_cursor,
            ])

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )


        observations = []
        

        for line in result.stdout.splitlines():

            if not line.strip():
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            cursor = entry.get("__CURSOR")

            if not cursor:
                continue

            

            timestamp = self._parse_timestamp(
                entry.get("__REALTIME_TIMESTAMP")
            )

            message = self._parse_message(
                entry.get("MESSAGE")
            )

            #Keep entity_id short and Galaxy-oriented. Keep the full journald cursor as metadata and later as collector state.
            log_id = hashlib.sha256(
                cursor.encode("utf-8")
            ).hexdigest()[:16]

            observations.append(
                Observation(
                    source="journald",
                    entity_type="log",
                    #entity_id=f"journal:{cursor}",
                    entity_id=log_id,
                    timestamp=timestamp,
                    data={
                        "journal_cursor": cursor,
                        "message": message,
                        "priority": self._to_int(
                            entry.get("PRIORITY")
                        ),
                        "service": entry.get(
                            "_SYSTEMD_UNIT"
                        ),
                        "pid": self._to_int(
                            entry.get("_PID")
                        ),
                        "process": entry.get(
                            "_COMM"
                        ),
                        "executable": entry.get(
                            "_EXE"
                        ),
                        "hostname": entry.get(
                            "_HOSTNAME"
                        ),
                        "identifier": entry.get(
                            "SYSLOG_IDENTIFIER"
                        ),
                    },
                )
            )


        # if observations:
        #     self.last_cursor = (
        #         observations[-1].entity_id.removeprefix(
        #             "journal:"
        #         )
        #     )
            # journal entry
            #     ↓
            # cursor = entry["__CURSOR"]
            #     ↓
            # create log_id from cursor
            #     ↓
            # store cursor in data["journal_cursor"]
            #     ↓
            # create Observation
            #     ↓
            # after loop:
            #     ↓
            # self.last_cursor = last observation's journal_cursor

            
        if observations:
            self.last_cursor = observations[-1].data["journal_cursor"]

        return observations

    def _parse_timestamp(self, value):

        if not value:
            return datetime.now(timezone.utc)

        try:
            microseconds = int(value)

            return datetime.fromtimestamp(
                microseconds / 1_000_000,
                tz=timezone.utc,
            )

        except (ValueError, TypeError, OverflowError):

            return datetime.now(timezone.utc)

    def _parse_message(self, value):

        if value is None:
            return None

        if isinstance(value, list):

            try:
                return bytes(value).decode(
                    "utf-8",
                    errors="replace",
                )
            except (ValueError, TypeError):
                return str(value)

        return str(value)

    def _to_int(self, value):

        if value is None:
            return None

        try:
            return int(value)
        except (ValueError, TypeError):
            return None
