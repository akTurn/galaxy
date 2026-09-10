from collectors.process import ProcessCollector
from core.graph.process_identity_map import ProcessIdentityMap
from core.graph.process_tree import ProcessTree
from core.storage.sqlite_store import SQLiteStore

# Exactly — **`observations` is the list of `Observation` objects that came from your `ProcessCollector`.**

# I should have shown where it comes from.

# Your flow is:

# ```text
# ProcessCollector
#       ↓
# observations
#       ↓
# ProcessIdentityMap
#       ↓
# ProcessTree
# ```

# For example, in a test you would have:


# ### What exactly is `observations`?

# When you do:

# ```python
# observations = collector.collect()
# ```

# you get something conceptually like:

# ```text
# observations = [
#     Observation(
#         entity_id="pid:1@1789035741.55",
#         data={"pid": 1, "name": "systemd", ...}
#     ),

#     Observation(
#         entity_id="pid:2@1789035741.55",
#         data={"pid": 2, "name": "init-systemd", ...}
#     ),

#     Observation(
#         entity_id="pid:1546@1789035741.55",
#         data={"pid": 1546, "name": "python", ...}
#     ),

#     ...
# ]
# ```

# Then:

# ```python
# identity_map = ProcessIdentityMap(observations)
# ```

# loops through those observations:

# ```python
# for observation in observations:
# ```

# and creates:

# ```text
# PID 1     → pid:1@1789035741.55
# PID 2     → pid:2@1789035741.55
# PID 1546   → pid:1546@1789035741.55
# ```

# So when we later say:

# ```python
# tree.get_tree(1)
# ```

# the `ProcessTree` does:

# ```python
# root_entity_id = self.identity_map.get(1)
# ```

# which gives:

# ```text
# pid:1@1789035741.55
# ```

# instead of incorrectly constructing:

# ```text
# pid:1
# ```

# ---

# ### One important thing

# Your **Orchestrator already has `observations`** because it does something like:

# ```python
# all_observations = []

# all_observations.extend(
#     self.process_collector.collect()
# )
# ```

# So  don't need to invent another source for it.

# The question now is simply:

# > **Where do we want to test/use `ProcessTree`?**

# For our next step, I'd recommend creating a small:

# ```text
# tests/test_process_tree.py
# ```

# that uses the existing `ProcessCollector`, `ProcessIdentityMap`, and `SQLiteStore`.



# 1. Collect current processes
collector = ProcessCollector()
observations = collector.collect()

# 2. Build PID → full entity ID mapping
identity_map = ProcessIdentityMap(observations)

# 3. Open Galaxy database
store = SQLiteStore()

# 4. Create process tree
tree = ProcessTree(store, identity_map)

# 5. Build tree starting from PID 1
process_tree = tree.get_tree(573)

print(process_tree)






#1.display tree function called

# def main():

#     store = SQLiteStore()

#     process_tree = ProcessTree(store)

#     tree_data = process_tree.get_tree(1539)

#     display = ProcessTreeDisplay()

#     display.print_tree(tree_data)


# if __name__ == "__main__":
#     main()



#2.Method inline display function

# def print_treetest(node, prefix=""):
#     print(prefix + node["entity_id"])

#     for child in node["children"]:
#         print_treetest(child, prefix + "  ")


# tree = ProcessTree(store)

# result = tree.get_tree(1539)

# print_treetest(result)


# #print(result)