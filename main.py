from core.orchestrator import Orchestrator
from core.storage.sqlite_store import SQLiteStore
from core.graph.machine_graph_display import MachineGraphDisplay
from core.correlation.correlation_engine import CorrelationEngine

import time


COLLECTION_INTERVAL_SECONDS = 10


def main():

    orchestrator = Orchestrator()
    store = SQLiteStore()
    correlation_engine = CorrelationEngine(store)
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
            # Collection summary
            # ----------------------------------------

            print(
                f"[{timestamp}] "
                f"Collected {len(observations)} observations, "
                f"derived {len(relationships)} relationships"
            )

            # ----------------------------------------
            # Corelation 
            # ----------------------------------------
            
            correlation_events = correlation_engine.analyze()

            if correlation_events:

                print()
                print("CORRELATION EVENTS")
                print("------------------")

                for event in correlation_events:

                    print(
                        event
                    )

                print()

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