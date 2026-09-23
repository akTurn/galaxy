from core.storage.sqlite_store import SQLiteStore
from core.graph.machine_graph import MachineGraph


class MachineGraphDisplay:

    def print_relationship_graph(self, store):
        """
        13E - Print the current relationship graph.

        Relationships returned by SQLiteStore.current_relationships()
        are tuples in the form:

            (
                source_type,
                source_id,
                relationship_type,
                target_type,
                target_id,
                timestamp
            )

        The graph is grouped by the complete source entity identity
        (type + id), so different entity types cannot collide.
        """

        relationships = store.current_relationships()

        if not relationships:
            print("No current relationships found.")
            return

        grouped = {}

        for relationship in relationships:

            (
                source_type,
                source_id,
                relationship_type,
                target_type,
                target_id,
                timestamp,
            ) = relationship

            source = f"{source_type}:{source_id}"
            target = f"{target_type}:{target_id}"

            grouped.setdefault(source, []).append(
                {
                    "type": relationship_type,
                    "target": target,
                }
            )

        print("\nCURRENT RELATIONSHIP GRAPH")
        print("==========================")

        relationship_count = 0

        for source, targets in sorted(grouped.items()):

            print(f"\n{source}")

            for relation in sorted(
                targets,
                key=lambda item: (
                    item["type"],
                    item["target"],
                ),
            ):

                print(
                    f"  └── {relation['type']} ──> "
                    f"{relation['target']}"
                )

                relationship_count += 1

        print("\n==========================")
        print(f"Sources: {len(grouped)}")
        print(f"Relationships: {relationship_count}")


    def _display_relationship_type(self, relationship_type, direction):
        if direction == "out":
            return relationship_type

        inverse_relationships = {
            "parent_of": "child_of",
            "runs": "run_by",
            "manages": "managed_by",
            "generated_by": "generates",
            "associated_with": "associated_with",
            "listens_on": "listened_on_by",
            "has_connection": "connection_of",
        }

        return inverse_relationships.get(
            relationship_type,
            relationship_type,
        )






    def traverse_relationships(
        self,
        store,
        start_entity_id,
        max_depth=5,
    ):
        """
        13F - Traverse the current relationship graph.

        Supports one-to-many relationships.

        Example:

            service:nginx
                -> process:pid:227@...
                -> process:pid:301@...

        The traversal uses the complete entity identity
        (entity_type + entity_id) and protects against cycles.
        """

        relationships = store.current_relationships()

        if not relationships:
            print("No current relationships found.")
            return

        # -------------------------------------------------
        # Build adjacency list
        # -------------------------------------------------
        #
        # Complete entity identity:
        #
        #     source_type + source_id
        #
        # This is important because an entity_id by itself
        # is not necessarily globally unique.
        #

        graph = {}

        for relationship in relationships:

            (
                source_type,
                source_id,
                relationship_type,
                target_type,
                target_id,
                timestamp,
            ) = relationship

            source = f"{source_type}:{source_id}"
            target = f"{target_type}:{target_id}"

            # graph.setdefault(source, []).append(
            #     {
            #         "type": relationship_type,
            #         "target": target,
            #     }
            # )

            graph.setdefault(source, []).append(
                {
                    "type": relationship_type,
                    "target": target,
                    "direction": "out",
                }
            )

            graph.setdefault(target, []).append(
                {
                    "type": relationship_type,
                    "target": source,
                    "direction": "in",
                }
            )

        # -------------------------------------------------
        # Normalise the starting entity
        # -------------------------------------------------

        start = start_entity_id

        # -------------------------------------------------
        # Traverse
        # -------------------------------------------------

        visited = set()

        def walk(entity_id, depth):

            indent = "  " * depth

            print(f"{indent}{entity_id}")

            if depth >= max_depth:
                print(f"{indent}  [max depth reached]")
                return

            if entity_id in visited:
                print(f"{indent}  [already visited]")
                return

            visited.add(entity_id)

            outgoing = graph.get(entity_id, [])

            for relationship in sorted(
                outgoing,
                key=lambda item: (
                    item["type"],
                    item["target"],
                ),
            ):

                #relationship_type = relationship["type"]
                relationship_type = self._display_relationship_type(
                    relationship["type"],
                    relationship["direction"],
                )

                target = relationship["target"]
                direction = relationship["direction"]
                target = relationship["target"]
                direction = relationship["direction"]

                if direction == "out":
                    arrow = f"── {relationship_type} ──>"
                else:
                    arrow = f"<── {relationship_type} ──"

                print(
                    f"{indent}  └── "
                    f"{arrow} "
                    f"{target}"
                )

                # print(
                #     f"{indent}  └── "
                #     f"{relationship_type} ──> "
                #     f"{target}"
                # )

                walk(target, depth + 1)

        print("\nRELATIONSHIP TRAVERSAL")
        print("=====================")

        walk(start, 0)

        print("=====================")