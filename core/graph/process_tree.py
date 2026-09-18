from core.storage.sqlite_store import SQLiteStore



class ProcessTree:

    def __init__(self, store: SQLiteStore,identity_map):
        self.store = store
        self.identity_map = identity_map

        # get_tree(root_pid)
        #         │
        #         │ root_pid = 1234
        #         ▼
        # identity_map.get(1234)
        #         │
        #         │ returns
        #         ▼
        # "pid:1234@4567.89"
        #         │
        #         │ stored in
        #         ▼
        # root_entity_id


    def get_tree(self, root_pid):

         # root_entity_id = f"pid:{root_pid}"

        root_entity_id = self.identity_map.get(root_pid)#convert pid to entityId

        if root_entity_id is None:
            return None    #handles a PID that doesn't exist anymore.   
       
        return self._build_tree(root_entity_id)

    def _build_tree(self, entity_id):

        children = self.store.get_children(entity_id)

        tree = {
            "entity_id": entity_id,
            "children": []
        }

        for child in children:

            child_entity_id = child[4]
            # 0 → source_entity_type
            # 1 → source_entity_id
            # 2 → relationship_type
            # 3 → target_entity_type
            # 4 → target_entity_id
            # 5 → timestamp

            # So child[4] is still the target/child identity.

            child_tree = self._build_tree(
                child_entity_id
            )#Recursion

            tree["children"].append(child_tree)

        return tree


        # ProcessIdentityMap = "Which entity represents this PID?"

        # SQLiteStore = "Which entities are children of this entity?"

        # ProcessTree = "Put those relationships together into a nested tree."


        #               observations                    
        #                │
        #                ▼
        #      ProcessIdentityMap
        #                │
        #                │
        #       100 → entity-A
        #                │
        #                │
        #                ▼
        #       process_tree.get_tree(100)
        #                │
        #                ▼
        #   identity_map.get(100)
        #                │
        #                ▼
        #           entity-A
        #                │
        #                ▼
        #     _build_tree(entity-A)
        #                │
        #                ▼
        #  store.get_children(entity-A)
        #                │
        #        ┌───────┴───────┐
        #        ▼               ▼
        #    entity-B         entity-C
        #        │               │
        #        ▼               ▼
        #  _build_tree(B)  _build_tree(C)
        #        │               │
        #        ▼               ▼
        #      children        children
        #        │               │
        #        └───────┬───────┘
        #                ▼
        #          nested dictionary

        # PID
        # │
        # │ ProcessIdentityMap
        # ▼
        # Entity ID
        # │
        # │ SQLiteStore
        # ▼
        # Children
        # │
        # │ recursion
        # ▼
        # Complete process tree
