class ProcessTreeDisplay:

    def print_tree(self, tree):
        self._print_node(tree, "", True)

    def _print_node(self, node, prefix, is_last):

        connector = "└── " if is_last else "├── "

        print(prefix + connector + node["entity_id"])

        children = node["children"]

        for index, child in enumerate(children):

            last = index == len(children) - 1

            if is_last:
                child_prefix = prefix + "    "
            else:
                child_prefix = prefix + "│   "

            self._print_node(
                child,
                child_prefix,
                last
            )
