from datetime import datetime, timezone
import subprocess

from core.models.observation import Observation


class DatabaseTableCollector:


    def collect(self):

        observations = []

        databases = self._get_databases()


        for database in databases:

            observations.extend(
                self._collect_tables(database)
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
            db.strip()
            for db in result.stdout.splitlines()
            if db.strip()
        ]



    def _collect_tables(self, database):

        observations = []


        result = subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                "-d",
                database,
                "-t",
                "-A",
                "-F",
                "|",
                "-c",
                """
                SELECT
                    schemaname,
                    tablename
                FROM pg_tables
                WHERE schemaname NOT IN
                (
                    'pg_catalog',
                    'information_schema'
                );
                """
            ],
            capture_output=True,
            text=True
        )


        now = datetime.now(timezone.utc)


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            schema, table = line.split("|")


            observations.append(
                Observation(
                    source="database",
                    entity_type="database_table",
                    entity_id=(
                        f"postgresql:"
                        f"{database}:"
                        f"{schema}:"
                        f"{table}"
                    ),
                    timestamp=now,
                    data={
                        "database":{
                            "engine":"postgresql",
                            "name":database
                        },
                        "table":{
                            "schema":schema,
                            "name":table
                        }
                    }
                )
            )


        return observations