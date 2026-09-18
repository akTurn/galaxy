#tests/test_store.py

from core.storage.sqlite_store import SQLiteStore


store = SQLiteStore()

print("Total observations:")
print(store.count())

print()

print("Latest observation:")
latest = store.latest()

print(latest)

if latest:
    print()
    print("Source:", latest.source)
    print("Entity type:", latest.entity_type)
    print("Entity ID:", latest.entity_id)
    print("Timestamp:", latest.timestamp)
    print("Data:", latest.data)


# --------------------------------------------------
# Services
# --------------------------------------------------

services = [
    observation
    for observation in store.all()
    if observation.entity_type == "service"
]

print()
print("=" * 60)
print("Services")
print("=" * 60)

print("Services stored:", len(services))

for service in services[:20]:
    print()
    print("Entity:", service.entity_id)
    print("State:", service.data.get("active_state"))
    print("Sub-state:", service.data.get("sub_state"))
    print("Main PID:", service.data.get("main_pid"))


# --------------------------------------------------
# Services with live MainPID
# --------------------------------------------------

live_services = [
    service
    for service in services
    if service.data.get("main_pid")
]

print()
print("=" * 60)
print("Services with live MainPID")
print("=" * 60)

print("Count:", len(live_services))

for service in live_services:
    print(
        service.entity_id,
        "-> PID",
        service.data["main_pid"]
    )


# --------------------------------------------------
# Processes
# --------------------------------------------------

processes = [
    observation
    for observation in store.all()
    if observation.entity_type == "process"
]

process_pids = set()

for process in processes:

    pid = process.data.get("pid")

    if pid is not None:
        process_pids.add(pid)


# --------------------------------------------------
# Verify Service -> Process candidates
# --------------------------------------------------

print()
print("=" * 60)
print("Service -> Process verification")
print("=" * 60)

for service in live_services:

    pid = service.data["main_pid"]

    if pid in process_pids:
        print(
            "OK:",
            service.entity_id,
            "-> PID",
            pid,
            "exists in process observations"
        )
    else:
        print(
            "MISSING:",
            service.entity_id,
            "-> PID",
            pid,
            "not found in process observations"
        )


# from core.storage.sqlite_store import SQLiteStore


# store = SQLiteStore()

# print("Total observations:")
# print(store.count())

# print()

# print("Latest observation:")
# latest = store.latest()

# print(latest)

# if latest:
#     print()
#     print("Source:", latest.source)
#     print("Entity type:", latest.entity_type)
#     print("Entity ID:", latest.entity_id)
#     print("Timestamp:", latest.timestamp)
#     print("Data:", latest.data)

