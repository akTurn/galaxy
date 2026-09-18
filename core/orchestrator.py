
from collectors.system import SystemCollector
from collectors.process import ProcessCollector
from collectors.network import NetworkCollector
from collectors.service import ServiceCollector
from core.storage.sqlite_store import SQLiteStore
from core.relationships.process import process_relationships
from core.relationships.network import network_relationships
from core.relationships.service import service_relationships
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
        # 6. Network relationships
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
        # 7.Service relationships
        # -------------------------

        service_observations = [
            observation
            for observation in all_observations
            if observation.entity_type == "service"
        ]

        for observation in service_observations:

            relationships = service_relationships(
                observation,
                identity_map
            )

            all_relationships.extend(
                relationships
            )


        # -------------------------
        # 8. Save relationships
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


    



    
