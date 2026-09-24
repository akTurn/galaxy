from datetime import datetime, timezone
import subprocess
import json

from core.models.observation import Observation


class DatabaseLockCollector:


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
                    'locktype', locktype,
                    'mode', mode,
                    'granted', granted,
                    'relation', relation
                )
                FROM pg_locks;
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


            pid = data["pid"]
            relation = data["relation"]


            observations.append(
                Observation(
                    source="database",
                    entity_type="database_lock",
                    #entity_id=f"postgresql:lock:{pid}:{relation}",
                    entity_id=(
                        f"postgresql:lock:"
                        f"{pid}:"
                        f"{data['locktype']}:"
                        f"{data['mode']}:"
                        f"{relation}"
                    ),
                    timestamp=now,
                    data={
                        "database":{
                            "engine":"postgresql",
                            "host":"localhost",
                        },
                        "lock":{
                            "pid":pid,
                            "locktype":data["locktype"],
                            "mode":data["mode"],
                            "granted":data["granted"],
                            "relation":relation,
                        }
                    }
                )
            )


        return observations
