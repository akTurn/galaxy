from collectors.database.connection import DatabaseConnectionCollector
from collectors.database.query import DatabaseQueryCollector
from collectors.database.lock import DatabaseLockCollector
from collectors.database.table import DatabaseTableCollector
from collectors.database.instance import DatabaseInstanceCollector
from collectors.database.health import DatabaseHealthCollector
from collectors.database.index import DatabaseIndexCollector


class DatabaseManager:

    def __init__(self):

        self.connection_collector = DatabaseConnectionCollector()
        self.query_collector = DatabaseQueryCollector()
        self.lock_collector = DatabaseLockCollector()
        self.table_collector = DatabaseTableCollector()
        self.instance_collector = DatabaseInstanceCollector()
        self.health_collector = DatabaseHealthCollector()
        self.index_collector = DatabaseIndexCollector()

        


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

        # database query observations
        observations.extend(
        self.query_collector.collect()
        )

        # database lock observations
        observations.extend(
            self.lock_collector.collect()
        )
        
         # database Instance observations
        database_instances = self.instance_collector.collect()

        observations.extend(
            self.instance_collector.collect()
        )

        # database table observations
        observations.extend(
            self.table_collector.collect()
        )

        # database health observations
        observations.extend(
            self.health_collector.collect()
        )

        # database index observations

        # observations.extend(
        #     self.index_collector.collect()
        # )

        
        # indexes
        for instance in database_instances:

            database_name = (
                instance.data["database"]["name"]
            )

            observations.extend(
                self.index_collector.collect(database_name)
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