from core.orchestrator import Orchestrator
import time

COLLECTION_INTERVAL_SECONDS = 10


def main():
    orchestrator = Orchestrator()

    print("GALAXY")
    print("======")
    print(f"Collecting every {COLLECTION_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")
    print()

    try:
        while True:

            
            timestamp = time.strftime("%H:%M:%S")

            #observations = orchestrator.run_once() # All Observations
            # print(
            #     f"[{timestamp}] Collected "
            #     f"{len(observations)} observations"
            # )


            #collected, total =orchestrator.run_once()#currently collected observation + overall db count
            
            # print(f"[{timestamp}] Collected {collected} observations "
            #    f"(total in storage: {total})")

            observations, relationships = orchestrator.run_once()

            print(
                f"[{timestamp}] "
                f"Collected {len(observations)} observations, "
                f"derived {len(relationships)} relationships"
            )            

            time.sleep(COLLECTION_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print()
        print("Galaxy stopped.")


if __name__ == "__main__":
    main()
