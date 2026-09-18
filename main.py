from core.orchestrator import Orchestrator
from core.storage.sqlite_store import SQLiteStore
from core.graph.machine_graph_display import MachineGraphDisplay

import time


COLLECTION_INTERVAL_SECONDS = 10


def main():

    orchestrator = Orchestrator()
    store = SQLiteStore()
    display = MachineGraphDisplay()

    print("GALAXY")
    print("======")
    print(
        f"Collecting every "
        f"{COLLECTION_INTERVAL_SECONDS} seconds. "
        f"Press Ctrl+C to stop."
    )
    print()

    try:

        while True:

            timestamp = time.strftime("%H:%M:%S")

            # ----------------------------------------
            # Collect observations and relationships
            # ----------------------------------------

            observations, relationships = orchestrator.run_once()

            # ----------------------------------------
            # Read services from storage
            # ----------------------------------------

            services = [
                observation
                for observation in store.all()
                if observation.entity_type == "service"
            ]

            print("Services stored:", len(services))

            for service in services[:10]:

                print(
                    service.entity_id,
                    service.data
                )

            # ----------------------------------------
            # Collection summary
            # ----------------------------------------

            print(
                f"[{timestamp}] "
                f"Collected {len(observations)} observations, "
                f"derived {len(relationships)} relationships"
            )

            # ----------------------------------------
            # Display machine graph
            # ----------------------------------------

            display.print_relationship_graph(store)

            # ----------------------------------------
            # Wait before next collection
            # ----------------------------------------

            time.sleep(COLLECTION_INTERVAL_SECONDS)

    except KeyboardInterrupt:

        print()
        print("Galaxy stopped.")


if __name__ == "__main__":
    main()