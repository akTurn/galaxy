from core.storage.sqlite_store import SQLiteStore
from core.graph.machine_graph import MachineGraph


def print_separator(title):
    print()
    print(title)
    print("=" * len(title))


def main():

    store = SQLiteStore()
    graph = MachineGraph(store)

    # --------------------------------------------------
    # 1. Current relationships
    # --------------------------------------------------

    print_separator("Current Relationships")

    relationships = graph.get_current_relationships()

    print("Current relationships:", len(relationships))

    for relationship in relationships[:20]:

        print(
            relationship[0],
            relationship[1],
            "->",
            relationship[2],
            "->",
            relationship[3],
            relationship[4],
        )

    # --------------------------------------------------
    # 2. Current neighbors of nginx
    # --------------------------------------------------

    print_separator("Current Neighbors")

    entity_id = "service:nginx"

    neighbors = graph.get_current_neighbors(entity_id)

    print("Entity:", entity_id)
    print("Neighbors:", len(neighbors))

    for neighbor in neighbors:

        print(
            neighbor["direction"],
            neighbor["relationship"],
            neighbor["entity_id"],
        )

    # --------------------------------------------------
    # 3. Current machine graph traversal
    # --------------------------------------------------

    print_separator("Current Machine Graph")

    tree = graph.traverse_current(
        entity_id,
        max_depth=3,
    )

    print(tree)

    # --------------------------------------------------
    # 4. Simple validation
    # --------------------------------------------------

    print_separator("Validation")

    assert relationships is not None

    assert neighbors is not None

    assert tree is not None

    assert tree["entity_id"] == entity_id

    print("Current relationships: PASS")
    print("Current neighbors: PASS")
    print("Current traversal: PASS")


if __name__ == "__main__":
    main()