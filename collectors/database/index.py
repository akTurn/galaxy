from datetime import datetime, timezone
import subprocess
import json

from core.models.observation import Observation


class DatabaseIndexCollector:


    def collect(self,database_name):

        observations = []

        observations.extend(
            self._collect_postgresql(database_name)
        )

        return observations



    def _collect_postgresql(self,database_name):

        observations = []

        now = datetime.now(timezone.utc)


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
                    schemaname,

                    'table',
                    tablename,

                    'index',
                    indexname,

                    'definition',
                    indexdef
                )
                FROM pg_indexes
                WHERE schemaname NOT IN
                (
                    'pg_catalog',
                    'information_schema'
                );
                """
            ],
            capture_output=True,
            text=True,
            check=False,
        )


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            data = json.loads(line)


            schema = data["schema"]
            table = data["table"]
            index = data["index"]


            observations.append(

                Observation(

                    source="database",

                    entity_type="database_index",

                    # entity_id=(
                    #     f"postgresql:index:"
                    #     f"{schema}:"
                    #     f"{table}:"
                    #     f"{index}"
                    # ),
                    entity_id=(
                        f"postgresql:index:"
                        f"{database_name}:"
                        f"{schema}:"
                        f"{table}:"
                        f"{index}"
                    ),

                    timestamp=now,


                    data={

                        "database":{

                            "engine":"postgresql",
                            "name": database_name

                        },

                        "index":{

                            "schema":schema,

                            "table":table,

                            "name":index,

                            "definition":
                                data["definition"]

                        }

                    }

                )

            )


        return observations