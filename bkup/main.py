
from collectors.system import SystemCollector
from collectors.process import ProcessCollector
from core.storage.sqlite_store import SQLiteStore
import time



    COLLECTION_INTERVAL_SECONDS = 10

def run_once(collectors, store):

    all_observations = []

    for collector in collectors:
        all_observations.extend(collector.collect())

    store.save(all_observations)

    return len(all_observations), len(store.all())

def main():
    collectors = [
        SystemCollector(),
        ProcessCollector(),
    ]

    store = SQLiteStore()

    print("GALAXY")
    print("======")
    print(f"Collecting every {COLLECTION_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")
    print()

    try:
        while True:
            collected, total = run_once(collectors, store)

            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] Collected {collected} observations "
                  f"(total in storage: {total})")

            time.sleep(COLLECTION_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print()
        print("Galaxy stopped.")
    # collectors = [
    #     SystemCollector(),
    #     ProcessCollector(),
    # ]

    # all_observations = []

    # for collector in collectors:
    #     all_observations.extend(collector.collect())

    # print("GALAXY")
    # print("======")
    # print()

    # #  # Separate processes so we can sort them by CPU usage
    # # process_obs = [
    # #     o for o in all_observations if o.entity_type == "process"
    # # ]
    # # process_obs.sort(key=lambda o: o.data["cpu_percent"], reverse=True)


    # # print("Top processes by CPU:")
    # # for obs in process_obs[:10]:
    # #     print(obs)

    # print(f"Total observations: {len(all_observations)}")
    # print()

    # for observation in all_observations[:10]:
    #     print(observation)


if __name__ == "__main__":
    main()


# from collectors.process import ProcessCollector


# def main():
#     collector = ProcessCollector()

#     processes = collector.collect()

#     print("GALAXY")
#     print("======")
#     print()

#     print(f"Processes found: {len(processes)}")
#     print()

#     for process in processes[:10]:
#         print(process)


# if __name__ == "__main__":
#     main()