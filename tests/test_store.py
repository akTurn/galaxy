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

