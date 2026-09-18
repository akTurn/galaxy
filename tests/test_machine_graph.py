from core.storage.sqlite_store import SQLiteStore
from core.graph.machine_graph import MachineGraph


store = SQLiteStore()

graph = MachineGraph(store)

relationships = store.all_relationships()

print("Relationships:", len(relationships))

print()
print("Testing neighbors")
print("=================")

for relationship in relationships:

    entity_id = relationship[1]

    print()
    print("Entity:", entity_id)

    neighbors = graph.get_neighbors(entity_id)

    for neighbor in neighbors:

        print(
            " ",
            neighbor["direction"],
            neighbor["relationship"],
            neighbor["entity_id"],
        )

    break

service_id = "service:nginx"

print("Neighbors of:", service_id)

neighbors = graph.get_neighbors(service_id)

for neighbor in neighbors:

    print(
        neighbor["direction"],
        neighbor["relationship"],
        neighbor["entity_id"],
    )

tree = graph.traverse(
    "service:nginx",
    max_depth=3,
)

print(tree)
