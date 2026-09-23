from collectors.database.connection import DatabaseConnectionCollector


class DatabaseManager:

    def __init__(self):

        self.connection_collector = DatabaseConnectionCollector()


    def collect(self):

        observations = []

        # database engine observations
        observations.extend(
            self._collect_database_status()
        )

        # database connection observations
        observations.extend(
            self.connection_collector.collect()
        )

        return observations


    def _collect_database_status(self):

        from datetime import datetime, timezone
        from core.models.observation import Observation

        observations=[]

        now=datetime.now(timezone.utc)


        observations.append(
            Observation(
                source="database",
                entity_type="database",
                entity_id="postgresql:localhost",
                timestamp=now,
                data={
                    "identity":{
                        "engine":"postgresql",
                        "host":"localhost"
                    },
                    "state":{
                        "status":"running"
                    }
                }
            )
        )


        observations.append(
            Observation(
                source="database",
                entity_type="database",
                entity_id="mysql:localhost",
                timestamp=now,
                data={
                    "identity":{
                        "engine":"mysql",
                        "host":"localhost"
                    },
                    "state":{
                        "status":"running"
                    }
                }
            )
        )


        return observations