from datetime import datetime, timezone
import subprocess

from core.models.observation import Observation


class DatabaseInstanceCollector:

    def collect(self):

        observations = []

        databases = self._get_databases()

        now = datetime.now(timezone.utc)

        for database in databases:

            observations.append(
                Observation(
                    source="database",
                    entity_type="database_instance",
                    entity_id=f"postgresql:database:{database}",
                    timestamp=now,
                    data={
                        "database": {
                            "engine": "postgresql",
                            "name": database
                        }
                    }
                )
            )

        return observations

    def _get_databases(self):

        result = subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                "-t",
                "-A",
                "-c",
                """
                SELECT datname
                FROM pg_database
                WHERE datistemplate=false;
                """
            ],
            capture_output=True,
            text=True
        )

        return [
            database.strip()
            for database in result.stdout.splitlines()
            if database.strip()
        ]
