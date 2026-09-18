from core.storage.sqlite_store import SQLiteStore
from core.graph.network_graph import NetworkGraph


store = SQLiteStore()

graph = NetworkGraph(store)

entity_id = "pid:1625@1789378375.83"

# relationships = graph.get_relationships_from(
#     entity_id
# )

# print("Relationships from:")
# print(entity_id)

# for relationship in relationships:
#     print(relationship)

# connections = graph.get_relationships_from(
#     entity_id,
#     "has_connection",
# )
# connections1=graph.get_relationships_from(
#     entity_id,
#     "listens_on",
# )


# print()
# print("Connections:")

# for connection in connections1:
#     print(connection)


neighbors = graph.get_neighbors(
    entity_id
)

print()
print("Neighbors:")

for neighbor in neighbors:
    print(neighbor)

tree = graph.traverse(
    "pid:1625@1789378375.83",
    max_depth=2,
)

print(tree)



