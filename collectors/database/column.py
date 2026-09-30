from datetime import datetime, timezone
import subprocess
import json

from core.models.observation import Observation


class DatabaseColumnCollector:

    def collect(self):

        observations = []

        databases = self._get_databases()


        for database in databases:

            observations.extend(
                self._collect_postgresql(database)
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


    def _collect_postgresql(self, database_name):

        observations = []


        result = subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                "-d",
                database_name,
                "-t",
                "-A",
                "-c",
                """
SELECT json_build_object(

    'schema',
    n.nspname,

    'table',
    c.relname,

    'column',
    a.attname,

    'data_type',
    pg_catalog.format_type(a.atttypid, a.atttypmod),

    'nullable',
    CASE
        WHEN a.attnotnull THEN 'NO'
        ELSE 'YES'
    END

)

FROM pg_catalog.pg_attribute a

JOIN pg_catalog.pg_class c
ON a.attrelid = c.oid

JOIN pg_catalog.pg_namespace n
ON c.relnamespace = n.oid


WHERE a.attnum > 0

AND NOT a.attisdropped

AND c.relkind = 'r'

AND n.nspname NOT IN (
    'pg_catalog',
    'information_schema'
);

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


            data = json.loads(line)


            schema = data["schema"]
            table = data["table"]
            column = data["column"]


            observations.append(
                Observation(

                    source="database",

                    entity_type="database_column",

                    entity_id=(
                        f"postgresql:"
                        f"column:"
                        f"{schema}:"
                        f"{table}:"
                        f"{column}"
                    ),

                    timestamp=now,

                    data={

                        "database":{
                            "engine":"postgresql",
                            "host":"localhost",
                            "name":database_name,
                        },

                        "column":{

                            "schema":schema,

                            "table":table,

                            "name":column,

                            "data_type":data["data_type"],

                            "nullable":data["nullable"]

                        }
                    }
                )
            )


        return observations
