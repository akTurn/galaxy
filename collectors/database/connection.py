from datetime import datetime, timezone
import subprocess

from core.models.observation import Observation


class DatabaseConnectionCollector:


    def collect(self):

        observations = []

        observations.extend(
            self._collect_postgresql()
        )

        observations.extend(
            self._collect_mysql()
        )

        return observations


    def _collect_postgresql(self):

        observations = []

        result = subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                "-t",
                "-A",
                "-F",
                "|",
                "-c",
                """
                SELECT
                    pid,
                    usename,
                    datname,
                    state
                FROM pg_stat_activity;
                """
            ],
            capture_output=True,
            text=True,
            check=False,
        )


        now = datetime.now(timezone.utc)


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            parts = line.split("|")


            pid = parts[0]

            # user = parts[1] if len(parts) > 1 else None
            # database = parts[2] if len(parts) > 2 else None
            # state = parts[3] if len(parts) > 3 else None

            user = parts[1] or None if len(parts) > 1 else None
            database = parts[2] or None if len(parts) > 2 else None
            state = parts[3] or None if len(parts) > 3 else None


            observations.append(
                Observation(
                    source="database",
                    entity_type="database_connection",
                    entity_id=f"postgresql:connection:{pid}",
                    timestamp=now,
                    data={
                        "database": {
                            "engine": "postgresql",
                            "host": "localhost",
                        },
                        "connection": {
                            "pid": pid,
                            "user": user,
                            "database": database,
                            "state": state,
                        }
                    }
                )
            )


        return observations

    def _collect_mysql(self):

        observations = []

        result = subprocess.run(
            [
                "sudo",
                "mysql",
                "-N",
                "-B",
                "-e",
                "SHOW PROCESSLIST;"
            ],
            capture_output=True,
            text=True,
            check=False,
        )


        now = datetime.now(timezone.utc)


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            parts = line.split("\t")


            connection_id = parts[0]

            user = parts[1] if len(parts) > 1 else None
            host = parts[2] if len(parts) > 2 else None
            database = parts[3] if len(parts) > 3 else None
            command = parts[4] if len(parts) > 4 else None
            state = parts[6] if len(parts) > 6 else None


            observations.append(
                Observation(
                    source="database",
                    entity_type="database_connection",
                    entity_id=f"mysql:connection:{connection_id}",
                    timestamp=now,
                    data={
                        "database": {
                            "engine": "mysql",
                            "host": "localhost",
                        },
                        "connection": {
                            "id": connection_id,
                            "user": user,
                            "host": host,
                            "database": database,
                            "command": command,
                            "state": state,
                        }
                    }
                )
            )


        return observations