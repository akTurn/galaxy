class NetworkGraph:

    def __init__(self, store):
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
    

    def get_relationships_from(
        self,
        entity_id,
        relationship_type=None,
    ):

        relationships = self.store.all_relationships()

        # results = []

        # for relationship in relationships:
        #     if relationship[1] == entity_id:
        #         results.append(relationship)

        results = [
            relationship
            for relationship in relationships
            if relationship[1] == entity_id
        ]

        if relationship_type is not None:

            results = [
                relationship
                for relationship in results
                if relationship[2] == relationship_type
            ]

        return results

    # This is a specific question.

    #     It asks:

    #     "What connections does this process have?"

    #     Suppose:

    #     Process A ──has_connection──> Connection X
    #     Process A ──has_connection──> Connection Y

    #     Then:

    #     get_process_connections("Process A")

    #     returns the outgoing has_connection neighbors.

    #     It does this:

    #     self.get_neighbors(process_entity_id)

    #     First find everything connected to the process.

    #     Then:

    #     if neighbor["direction"] == "out"

    #     Only relationships going outward.

    #     And:

    #     and neighbor["relationship"] == "has_connection"

    #     Only has_connection.

    #     So:

    #     get_neighbors()
    #         ↓
    #     all neighbors
    #         ↓
    #     filter
    #         ↓
    #     out + has_connection
    #         ↓
    #     process connections



    def get_process_connections(self, process_entity_id):

        return [
            neighbor
            for neighbor in self.get_neighbors(process_entity_id)
            if neighbor["direction"] == "out"
            and neighbor["relationship"] == "has_connection"
        ]

    def get_connection_processes(self, connection_entity_id):

        results = []

        for neighbor in self.get_neighbors(connection_entity_id):

            if (
                neighbor["direction"] == "in"
                and neighbor["relationship"] == "has_connection"
            ):
                results.append(neighbor["entity_id"])

        return results



    # def get_connection_processes(self, connection_entity_id):

    #     results = []

    #     for relationship in self.store.all_relationships():

    #         source_id = relationship[1]
    #         relationship_type = relationship[2]
    #         target_id = relationship[4]

    #         if (
    #             target_id == connection_entity_id
    #             and relationship_type == "has_connection"
    #         ):

    #             results.append(source_id)

    #     return results

    def get_port_processes(self, port_entity_id):

        results = []

        for relationship in self.store.all_relationships():

            source_id = relationship[1]
            relationship_type = relationship[2]
            target_id = relationship[4]

            if (
                target_id == port_entity_id
                and relationship_type == "listens_on"
            ):

                results.append(source_id)

        return results


    #everything directly connected to this entity,
    # regardless of whether the relationship points toward it or away from it
    
    # For example:

    #         has_connection
    #     A ───────────────────> B

    #     If you ask:

    #     get_neighbors("A")

    #     you get B as an outgoing neighbor.

    #     If you ask:

    #     get_neighbors("B")

    #     you get A as an incoming neighbor.
    
    def get_neighbors( self,
        entity_id,
        relationships=None,):#sometimes you already have the relationships and don't want to query the database again

            if relationships is None:
                relationships = self.store.all_relationships()
                

            neighbors = []

            for relationship in relationships:

                source_id = relationship[1]
                target_id = relationship[4]
                #source-id perspective ie A is perspective so out
                if source_id == entity_id:
                    neighbors.append({
                        "direction": "out",
                        "relationship": relationship[2],
                        "entity_id": target_id,# B
                    })#A ──has_connection──> B
                #target-id perspective ie B is so direction is in
                elif target_id == entity_id:
                    neighbors.append({
                        "direction": "in",
                        "relationship": relationship[2],
                        "entity_id": source_id,# A
                    })#A ──has_connection──> B 

            return neighbors
    
    def traverse(self, root_entity_id, max_depth=3):

        relationships = self.store.all_relationships()

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

            for neighbor in self.get_neighbors(entity_id,relationships):

                child = walk(
                    neighbor["entity_id"],
                    depth + 1
                )

                if child is not None:

                    node["neighbors"].append({
                        "relationship": neighbor["relationship"],
                        "direction": neighbor["direction"],
                        "node": child,
                    })

            return node

        return walk(root_entity_id, 0)



    
