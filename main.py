from core.orchestrator import Orchestrator
#from core.storage.sqlite_store import SQLiteStore
from core.graph.machine_graph_display import MachineGraphDisplay
from core.graph.machine_graph import MachineGraph
from core.correlation.correlation_engine import (
    CorrelationEngine
)

from core.storage.finding_store import FindingStore





import time


COLLECTION_INTERVAL_SECONDS = 10


def main():

    orchestrator = Orchestrator()
    #store = SQLiteStore()

    #graph = MachineGraph(store)

    graph = MachineGraph(
    orchestrator.store
    )

    correlation_engine = CorrelationEngine(
        graph
    )

    display = MachineGraphDisplay()

    finding_store = FindingStore()
    

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
            # Correlation Analysis
            # ----------------------------------------

            findings = correlation_engine.analyze(
                observations
            )


            for finding in findings:

                print()
                print("====== GALAXY FINDING ======")
                               

                finding_store.save(
                        finding
                    )

                print(finding)


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

            #display.print_relationship_graph(store)

            # ----------------------------------------
            # Wait before next collection
            # ----------------------------------------

            time.sleep(COLLECTION_INTERVAL_SECONDS)

    except KeyboardInterrupt:

        print()
        print("Galaxy stopped.")


if __name__ == "__main__":
    main()