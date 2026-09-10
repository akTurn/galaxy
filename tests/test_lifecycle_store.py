from core.storage.sqlite_store import SQLiteStore


store = SQLiteStore()

events = store.all_lifecycle_events()

print("Total lifecycle events:")
print(len(events))

print()

for event in events[-10:]:
    print(event)

print("Recent starts:")
for event in store.get_recent_starts():
    print(event)

print("\nRecent exits:")
for event in store.get_recent_exits():
    print(event)

print("\nProcess history:")
for event in store.get_process_history("pid:1546@1789035741.55"):
    print(event)

