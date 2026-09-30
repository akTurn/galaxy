from datetime import datetime, timezone
import subprocess
import json

from core.models.observation import Observation


class DatabaseForeignKeyCollector:


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



    def _collect_postgresql(self, database):

        observations=[]


        result=subprocess.run(
            [
                "sudo",
                "-u",
                "postgres",
                "psql",
                "-d",
                database,
                "-t",
                "-A",
                "-c",
                """

SELECT json_build_object(

'constraint',
tc.constraint_name,

'from_schema',
tc.table_schema,

'from_table',
tc.table_name,

'from_column',
kcu.column_name,


'to_schema',
ccu.table_schema,

'to_table',
ccu.table_name,

'to_column',
ccu.column_name

)

FROM information_schema.table_constraints tc


JOIN information_schema.key_column_usage kcu

ON tc.constraint_name=kcu.constraint_name


JOIN information_schema.constraint_column_usage ccu

ON ccu.constraint_name=tc.constraint_name


WHERE tc.constraint_type='FOREIGN KEY';


"""
            ],
            capture_output=True,
            text=True
        )


        now=datetime.now(timezone.utc)


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            data=json.loads(line)


            observations.append(

                Observation(

                    source="database",

                    entity_type="database_foreign_key",

                    entity_id=(

                        f"postgresql:"
                        f"{database}:"
                        f"{data['from_table']}:"
                        f"{data['from_column']}:"
                        f"{data['to_table']}:"
                        f"{data['to_column']}"

                    ),

                    timestamp=now,


                    data={

                        "database":{

                            "engine":"postgresql",
                            "name":database

                        },


                        "foreign_key":data

                    }

                )

            )


        return observations
