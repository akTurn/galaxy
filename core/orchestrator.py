
from collectors.system import SystemCollector
from collectors.process import ProcessCollector
from collectors.network import NetworkCollector
from collectors.service import ServiceCollector
from collectors.log import LogCollector
from collectors.database.database import DatabaseManager
from core.storage.sqlite_store import SQLiteStore
from core.relationships.process import process_relationships
from core.relationships.network import network_relationships
from core.relationships.service import service_relationships
from core.relationships.log import log_relationships
from core.relationships.application import application_relationships
from collectors.unix_socket import UnixSocketCollector

from core.relationships.unix_socket import (
    query_unix_socket_relationships
)
from core.relationships.database import (
    database_session_relationships,
    database_service_relationships,
    database_process_relationships,
    application_database_relationships,
    database_query_relationships,
    database_lock_relationships,
    database_table_relationships,
    query_table_relationships,
    query_process_relationships,
    
)
from core.graph.process_identity_map import ProcessIdentityMap
from core.graph.process_lifecycle import ProcessLifecycleTracker
from core.models.lifecycle_event import LifecycleEvent

class Orchestrator: 

    
    

    def __init__(self):
        self.collectors = [
            SystemCollector(),
            ProcessCollector(),
            NetworkCollector(),
            ServiceCollector(),
            LogCollector(),
            DatabaseManager(),
            UnixSocketCollector(),

        ]
        self.store = SQLiteStore()
        self.lifecycle_tracker = ProcessLifecycleTracker()
        



    def run_once(self):

        all_observations = []
        

        # -------------------------
        # 1. Collect observations
        # -------------------------

        for collector in self.collectors:

            observations = collector.collect()

            all_observations.extend(observations)

        # -------------------------
        # 2. Save observations
        # -------------------------

        self.store.save(all_observations)

        # --------------------------------
        # 3. Select process observations
        # --------------------------------

        process_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "process"
        ]

        lifecycle = self.lifecycle_tracker.update(
            process_observations
        )

        lifecycle_events = []

        for entity_id in lifecycle["started"]:

            lifecycle_events.append(
                LifecycleEvent(
                    event_type="process_started",
                    entity_type="process",
                    entity_id=entity_id,
                    timestamp=process_observations[0].timestamp,
                )
            )

        for entity_id in lifecycle["exited"]:

            lifecycle_events.append(
                LifecycleEvent(
                    event_type="process_exited",
                    entity_type="process",
                    entity_id=entity_id,
                    timestamp=process_observations[0].timestamp,
                )
            )

        # --------------------------------
        # 4. Build identity map
        # --------------------------------

        identity_map = ProcessIdentityMap(
            process_observations
        )

        # -------------------------
        # 5. Derive relationships
        # -------------------------

        all_relationships = []

        for observation in process_observations:

            relationships = process_relationships(
                observation,
                identity_map
            )

            all_relationships.extend(
                relationships
            )


        # -------------------------
        # 6. Application relationships
        # -------------------------

        service_observations = [
                    observation
                    for observation in all_observations
                    if observation.entity_type == "service"
                ]
        

        applications, application_relationships_list = (
            application_relationships(
                process_observations,
                service_observations
            )
        )

        all_relationships.extend(
            application_relationships_list
        )

        # -------------------------
        # 7. Network relationships
        # -------------------------

        for observation in all_observations:

            if observation.entity_type not in (
                "listening_port",
                "network_connection",
            ):
                continue

            

            relationships = network_relationships(
                observation,
                identity_map
            )

            all_relationships.extend(
                relationships
            )
        # -------------------------
        # 8.Service relationships
        # -------------------------

        
        service_map = {
            observation.entity_id: observation
            for observation in service_observations
        }

        for observation in service_observations:

            relationships = service_relationships(
                observation,
                identity_map
            )

            all_relationships.extend(
                relationships
            )

        # -------------------------
        # 9. Log relationships
        # -------------------------

        log_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "log"
        ]

        for observation in log_observations:

            relationships = log_relationships(
                observation,
                identity_map,
                service_map
            )

            all_relationships.extend(
                relationships
            )

        # -------------------------
        # 10. Database relationships
        # -------------------------

        database_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "database"
        ]


        database_connection_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "database_connection"
        ]


        # Database → Connection

        for database in database_observations:

            relationships = database_session_relationships(
                database,
                database_connection_observations
            )

            all_relationships.extend(
                relationships
            )


        # Service → Database

        relationships = database_service_relationships(
            service_observations,
            database_observations
        )

        all_relationships.extend(
            relationships
        )


        # Process → Database

        process_db_relationships = database_process_relationships(
            process_observations,
            database_observations
        )

        all_relationships.extend(
            process_db_relationships
        )


        # Application → Database

        relationships = application_database_relationships(
            application_relationships_list,
            process_db_relationships
        )

        all_relationships.extend(
            relationships
        )


        # -------------------------
        # Database → Query relationships
        # -------------------------        

        query_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "database_query"
        ]


        for database in database_observations:

            relationships = database_query_relationships(
                database,
                query_observations
            )

            all_relationships.extend(
                relationships
            )



        # -------------------------
        # Database → Lock relationships
        # -------------------------

        lock_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "database_lock"
        ]


        for database in database_observations:

            relationships = database_lock_relationships(
                database,
                lock_observations
            )

            all_relationships.extend(
                relationships
            )



        # -------------------------
        # Database table relationships
        # -------------------------

        database_instance_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "database_instance"
        ]


        table_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "database_table"
        ]


        relationships = database_table_relationships(
            database_instance_observations,
            table_observations
        )

        all_relationships.extend(
            relationships
        )


        query_observations=[
            x for x in all_observations
            if x.entity_type=="database_query"
        ]

        # -------------------------
        # Query → table relationships
        # -------------------------
        
        # table_observations=[
        #     x for x in all_observations
        #     if x.entity_type=="database_table"
        # ]


        relationships = query_table_relationships(
            query_observations,
            table_observations
        )


        all_relationships.extend(
            relationships
        )

        # -------------------------
        # Query → Process relationships
        # -------------------------

        relationships = query_process_relationships(
            query_observations,
            process_observations
        )

        all_relationships.extend(
            relationships
        )

        
        unix_sockets_observations=[
                    x for x in all_observations
                    if x.entity_type=="unix_socket"
                ]

        unix_relationships = query_unix_socket_relationships(
            process_observations,
            unix_sockets_observations
        )

        all_relationships.extend(
            unix_relationships
        )
        


        # -------------------------
        # 10. Save relationships
        # -------------------------

        self.store.save_relationships(
            all_relationships
        )

        self.store.save_lifecycle_events(
            lifecycle_events
        )

        # print(
        #     f"Lifecycle: "
        #     f"{len(lifecycle['started'])} started, "
        #     f"{len(lifecycle['running'])} running, "
        #     f"{len(lifecycle['exited'])} exited"
        # )

        return all_observations, all_relationships





    
        # for observation in all_observations:

        #     if observation.entity_type == "process":

        #         relationships = process_relationships(
        #             observation
        #         )

        #         all_relationships.extend(relationships) 

    # def run_once(self):
    #     all_observations = []

    #     for collector in self.collectors:
    #         observations = collector.collect()
    #         all_observations.extend(observations)

    #     self.store.save(all_observations)

    #     #return all_observationsdef run_once(self):
    

    #     return len(all_observations), self.store.count()


    



    
