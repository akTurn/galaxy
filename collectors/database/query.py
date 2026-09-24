from datetime import datetime, timezone
import subprocess,json

from core.models.observation import Observation


class DatabaseQueryCollector:


    def collect(self):

        observations = []

        observations.extend(
            self._collect_postgresql()
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
                "-c",
                """
                SELECT json_build_object(
                    'pid', pid,
                    'user', usename,
                    'database', datname,
                    'state', state,
                    'query', query
                )
                FROM pg_stat_activity;
                """
                # "-t",
                # "-A",
                # "-F",
                # "|",
                # "-c",
                # """
                # SELECT
                #     pid,
                #     usename,
                #     datname,
                #     state,
                #     query
                # FROM pg_stat_activity
                # WHERE query IS NOT NULL;
                # """
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


            # pid = parts[0]
            # user = parts[1]
            # database = parts[2]
            # state = parts[3]
            # query = parts[4]


            # if len(parts) < 5:
            #     continue

            # pid = parts[0]
            # user = parts[1] or None
            # database = parts[2] or None
            # state = parts[3] or None
            # query = "|".join(parts[4:]) or None

            data = json.loads(line)

            pid = str(data["pid"])
            user = data["user"]
            database = data["database"]
            state = data["state"]
            query = data["query"] or None


            observations.append(
                Observation(
                    source="database",
                    entity_type="database_query",
                    entity_id=f"postgresql:query:{pid}",
                    timestamp=now,
                    data={
                        "database":{
                            "engine":"postgresql",
                            "host":"localhost",
                        },
                        "query":{
                            "pid":pid,
                            "user":user,
                            "database":database,
                            "state":state,
                            "sql":query,
                        }
                    }
                )
            )


        return observations