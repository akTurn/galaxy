from core.storage.sqlite_store import SQLiteStore


class MachineGraph:

    def __init__(self, store: SQLiteStore):
        self.store = store

    

    def get_current_relationships(self):

        return self.store.current_relationships()

    def get_current_neighbors(self, entity_id):

        relationships = self.store.current_relationships()

        return self.get_neighbors(
            entity_id,
            relationships,
        )

    def traverse_current(self, root_entity_id, max_depth=3):

        relationships = self.store.current_relationships()

        visited = set()

        def walk(entity_id, depth):

            if depth > max_depth:
                return None

            if entity_id in visited:
                return None

            visited.add(entity_id)

            node = {
                "entity_id": entity_id,
                "neighbors": []
            }

            for neighbor in self.get_neighbors(
                entity_id,
                relationships,
            ):

                child = walk(
                    neighbor["entity_id"],
                    depth + 1,
                )

                if child is not None:

                    node["neighbors"].append({
                        "relationship": neighbor["relationship"],
                        "direction": neighbor["direction"],
                        "node": child,
                    })

            return node

        return walk(root_entity_id, 0)

    def _relationships(self):

        return self.store.all_relationships()

    def get_outgoing(self, entity_id):

        relationships = self._relationships()

        results = []

        for relationship in relationships:

            source_id = relationship[1]

            if source_id == entity_id:

                results.append(relationship)

        return results


    def get_incoming(self, entity_id):

        relationships = self._relationships()

        results = []

        for relationship in relationships:

            target_id = relationship[4]

            if target_id == entity_id:

                results.append(relationship)

        return results

    # def get_neighbors(self, entity_id):

    #     relationships = self._relationships()

    #     neighbors = []

    #     for relationship in relationships:

    #         source_id = relationship[1]
    #         relationship_type = relationship[2]
    #         target_id = relationship[4]

    #         if source_id == entity_id:

    #             neighbors.append({
    #                 "direction": "out",
    #                 "relationship": relationship_type,
    #                 "entity_id": target_id,
    #             })

    #         elif target_id == entity_id:

    #             neighbors.append({
    #                 "direction": "in",
    #                 "relationship": relationship_type,
    #                 "entity_id": source_id,
    #             })

    #     return neighbors


    # def get_neighbors(
    #     self,
    #     entity_id,
    #     relationship_type=None,
    # ):

    #     relationships = self._relationships()

    #     neighbors = []

    #     for relationship in relationships:

    #         source_id = relationship[1]
    #         current_relationship = relationship[2]
    #         target_id = relationship[4]

    #         if (
    #             relationship_type is not None
    #             and current_relationship != relationship_type
    #         ):
    #             continue

    #         if source_id == entity_id:

    #             neighbors.append({
    #                 "direction": "out",
    #                 "relationship": current_relationship,
    #                 "entity_id": target_id,
    #             })

    #         elif target_id == entity_id:

    #             neighbors.append({
    #                 "direction": "in",
    #                 "relationship": current_relationship,
    #                 "entity_id": source_id,
    #             })

    #     return neighbors

    def get_neighbors(
    self,
    entity_id,
    relationships=None,
    relationship_type=None,
    ):

        if relationships is None:
            relationships = self._relationships()

        neighbors = []

        for relationship in relationships:

            source_id = relationship[1]
            current_relationship = relationship[2]
            target_id = relationship[4]

            if (
                relationship_type is not None
                and current_relationship != relationship_type
            ):
                continue

            if source_id == entity_id:

                neighbors.append({
                    "direction": "out",
                    "relationship": current_relationship,
                    "entity_id": target_id,
                })

            elif target_id == entity_id:

                neighbors.append({
                    "direction": "in",
                    "relationship": current_relationship,
                    "entity_id": source_id,
                })

        return neighbors

    def traverse(self, root_entity_id, max_depth=3):

        visited = set()

        def walk(entity_id, depth):

            if depth > max_depth:
                return None

            if entity_id in visited:
                return None

            visited.add(entity_id)

            node = {
                "entity_id": entity_id,
                "neighbors": [],
            }

            neighbors = self.get_neighbors(entity_id)

            for neighbor in neighbors:

                child = walk(
                    neighbor["entity_id"],
                    depth + 1,
                )

                if child is None:
                    continue

                node["neighbors"].append({
                    "relationship": neighbor["relationship"],
                    "direction": neighbor["direction"],
                    "node": child,
                })

            return node

        return walk(root_entity_id, 0)
