from core.storage.sqlite_store import SQLiteStore
from collections import deque


class MachineGraph:

    def __init__(self, store: SQLiteStore):
        self.store = store

    

    # def get_current_relationships(self):

    #     return self.store.current_relationships()


    
    def _relationships(self, include_history=False):
        if include_history:
            return self.store.all_relationships()

        return self.store.current_relationships()

        
    def get_outgoing(
        self, entity_type, entity_id, include_history=False
    ):
        relationships = self._relationships(
            include_history=include_history
        )

        return [
            relationship
            for relationship in relationships
            if (
                relationship[0] == entity_type
                and relationship[1] == entity_id
            )
        ]


    def get_incoming(
        self, entity_type, entity_id, include_history=False
    ):
        relationships = self._relationships(
            include_history=include_history
        )

        return [
            relationship
            for relationship in relationships
            if (
                relationship[3] == entity_type
                and relationship[4] == entity_id
            )
        ]


    def impact_analysis(
        self, entity_type, entity_id, include_history=False
    ):
        incoming = self.get_incoming(
            entity_type, entity_id, include_history
        )

        outgoing = self.get_outgoing(
            entity_type, entity_id, include_history
        )

        return {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "affected_by": incoming,
            "affects": outgoing,
        }


    
    # def get_outgoing(self, entity_id, include_history=False):
    #     relationships = self._relationships(
    #         include_history=include_history
    #     )

    #     results = []

    #     for relationship in relationships:
    #         source_id = relationship[1]

    #         if source_id == entity_id:
    #             results.append(relationship)

    #     return results


    # def get_incoming(self, entity_id, include_history=False):
    #     relationships = self._relationships(
    #         include_history=include_history
    #     )

    #     results = []

    #     for relationship in relationships:
    #         target_id = relationship[4]

    #         if target_id == entity_id:
    #             results.append(relationship)

    #     return results

        
    # def get_neighbors(
    #     self,
    #     entity_id,
    #     relationships=None,
    #     relationship_type=None,
    #     include_history=False,
    # ):
    #     if relationships is None:
    #         relationships = self._relationships(
    #             include_history=include_history
    #         )

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
        entity_type,
        entity_id,
        relationships=None,
        relationship_type=None,
        include_history=False,
    ):
        if relationships is None:
            relationships = self._relationships(
                include_history=include_history
            )

        neighbors = []

        for relationship in relationships:
            source_type = relationship[0]
            source_id = relationship[1]
            current_relationship = relationship[2]
            target_type = relationship[3]
            target_id = relationship[4]

            if (
                relationship_type is not None
                and current_relationship != relationship_type
            ):
                continue

            # Current node is the source.
            if (
                source_type == entity_type
                and source_id == entity_id
            ):
                neighbors.append({
                    "entity_type": target_type,
                    "entity_id": target_id,
                    "direction": "out",
                    "relationship": current_relationship,
                })

            # Current node is the target.
            elif (
                target_type == entity_type
                and target_id == entity_id
            ):
                neighbors.append({
                    "entity_type": source_type,
                    "entity_id": source_id,
                    "direction": "in",
                    "relationship": current_relationship,
                })

        return neighbors





    # def get_current_neighbors(self, entity_id):

    #     relationships = self.store.current_relationships()

    #     return self.get_neighbors(
    #         entity_id,
    #         relationships,
    #     )

    # def traverse_current(self, root_entity_id, max_depth=3):

    #     relationships = self.store.current_relationships()

    #     visited = set()

    #     def walk(entity_id, depth):

    #         if depth > max_depth:
    #             return None

    #         if entity_id in visited:
    #             return None

    #         visited.add(entity_id)

    #         node = {
    #             "entity_id": entity_id,
    #             "neighbors": []
    #         }

    #         for neighbor in self.get_neighbors(
    #             entity_id,
    #             relationships,
    #         ):

    #             child = walk(
    #                 neighbor["entity_id"],
    #                 depth + 1,
    #             )

    #             if child is not None:

    #                 node["neighbors"].append({
    #                     "relationship": neighbor["relationship"],
    #                     "direction": neighbor["direction"],
    #                     "node": child,
    #                 })

    #         return node

    #     return walk(root_entity_id, 0)


    def find_entities(
        self,
        entity_type=None,
        keyword=None
    ):

        observations = self.store.all()

        results=[]

        for obs in observations:

            if entity_type:
                if obs.entity_type != entity_type:
                    continue


            if keyword:

                text = str(obs.data).lower()

                if keyword.lower() not in text:
                    continue


            results.append(obs)


    #     return results


    # def impact_analysis(self, entity_id, include_history=False):
    #     incoming = self.get_incoming(
    #         entity_id,
    #         include_history=include_history,
    #     )

    #     outgoing = self.get_outgoing(
    #         entity_id,
    #         include_history=include_history,
    #     )

    #     return {
    #         "affected_by": incoming,
    #         "affects": outgoing,
    #     }
    

    # def shortest_path(
    #     self,
    #     start_entity_id,
    #     target_entity_id,
    #     include_history=False,
    # ):
    #     relationships = self._relationships(
    #         include_history=include_history
    #     )


    #     queue = deque()

    #     queue.append(
    #         (
    #             start_entity_id,
    #             [start_entity_id]
    #         )
    #     )


    #     visited = set()

    #     visited.add(
    #         start_entity_id
    #     )


    #     while queue:


    #         current, path = queue.popleft()


    #         if current == target_entity_id:
    #             return path



    #         for neighbor in self.get_neighbors(
    #                 current,
    #                 relationships
    #         ):

    #             next_entity = neighbor["entity_id"]


    #             if next_entity not in visited:

    #                 visited.add(
    #                     next_entity
    #                 )

    #                 queue.append(
    #                     (
    #                         next_entity,
    #                         path + [next_entity]
    #                     )
    #                 )


    #     return []


    
    def shortest_path(
        self,
        start_entity_type,
        start_entity_id,
        target_entity_type,
        target_entity_id,
        include_history=False,
    ):
        relationships = self._relationships(
            include_history=include_history
        )

        start = (start_entity_type, start_entity_id)
        target = (target_entity_type, target_entity_id)

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()

            if current == target:
                return path

            current_type, current_id = current

            neighbors = self.get_neighbors(
                current_type,
                current_id,
                relationships=relationships,
            )

            for neighbor in neighbors:
                next_node = (
                    neighbor["entity_type"],
                    neighbor["entity_id"],
                )

                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((
                        next_node,
                        path + [next_node],
                    ))

        return []


    
    # def traverse(
    #     self,
    #     root_entity_id,
    #     max_depth=3,
    #     include_history=False,
    # ):
    #     relationships = self._relationships(
    #         include_history=include_history
    #     )

    #     visited = set()

    #     def walk(entity_id, depth):
    #         if depth > max_depth:
    #             return None

    #         if entity_id in visited:
    #             return None

    #         visited.add(entity_id)

    #         node = {
    #             "entity_id": entity_id,
    #             "neighbors": [],
    #         }

    #         neighbors = self.get_neighbors(
    #             entity_id,
    #             relationships=relationships,
    #         )

    #         for neighbor in neighbors:
    #             child = walk(
    #                 neighbor["entity_id"],
    #                 depth + 1,
    #             )

    #             if child is None:
    #                 continue

    #             node["neighbors"].append({
    #                 "relationship": neighbor["relationship"],
    #                 "direction": neighbor["direction"],
    #                 "node": child,
    #             })

    #         return node

    #     return walk(root_entity_id, 0)


        
    def traverse(
        self,
        root_entity_type,
        root_entity_id,
        max_depth=3,
        include_history=False,
    ):
        relationships = self._relationships(
            include_history=include_history
        )

        visited = set()

        def walk(entity_type, entity_id, depth):
            if depth > max_depth:
                return None

            node_key = (entity_type, entity_id)

            if node_key in visited:
                return None

            visited.add(node_key)

            node = {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "neighbors": [],
            }

            neighbors = self.get_neighbors(
                entity_type,
                entity_id,
                relationships=relationships,
            )

            for neighbor in neighbors:
                child = walk(
                    neighbor["entity_type"],
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

        return walk(root_entity_type, root_entity_id, 0)


    
    def get_current_neighbors(
        self,
        entity_type,
        entity_id,
        relationship_type=None,
    ):
        relationships = self.store.current_relationships()

        return self.get_neighbors(
            entity_type,
            entity_id,
            relationships=relationships,
            relationship_type=relationship_type,
        )


        
    def traverse_current(
        self,
        root_entity_type,
        root_entity_id,
        max_depth=3,
    ):
        relationships = self.store.current_relationships()

        visited = set()

        def walk(entity_type, entity_id, depth):
            if depth > max_depth:
                return None

            node_key = (entity_type, entity_id)

            if node_key in visited:
                return None

            visited.add(node_key)

            node = {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "neighbors": [],
            }

            neighbors = self.get_neighbors(
                entity_type,
                entity_id,
                relationships=relationships,
            )

            for neighbor in neighbors:
                child = walk(
                    neighbor["entity_type"],
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

        return walk(root_entity_type, root_entity_id, 0)




