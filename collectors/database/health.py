from datetime import datetime, timezone
import subprocess

from core.models.observation import Observation


class DatabaseHealthCollector:


    def collect(self):

        observations = []

        observations.extend(
            self._postgresql_health()
        )

        return observations



    def _postgresql_health(self):

        observations = []

        now = datetime.now(timezone.utc)


        try:

            result = subprocess.run(
                [
                    "sudo",
                    "-u",
                    "postgres",
                    "psql",
                    "-t",
                    "-A",
                    "-c",
                    "SELECT 1;"
                ],
                capture_output=True,
                text=True,
                timeout=5
            )


            if result.stdout.strip() == "1":

                status = "healthy"

            else:

                status = "unhealthy"



        except Exception:

            status = "unreachable"



        observations.append(

            Observation(

                source="database",

                entity_type="database_health",

                entity_id="postgresql:health:localhost",

                timestamp=now,

                data={

                    "database":{

                        "engine":"postgresql",

                        "host":"localhost"

                    },

                    "health":{

                        "status":status

                    }

                }

            )

        )


        return observations