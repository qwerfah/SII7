from tree.node import Node
from typing import Dict, List

from dialog_system.search_params import SearchParams


class Tree:
    root: Node

    def __init__(self, json: Dict):
        if "root" in json:
            self.root = Node(json["root"])
        else:
            raise ValueError("No root in json-object")

    def get_node(self, name: str, node: Node = None) -> Node:
        node = self.root if node is None else node

        if node is not None:
            return node

        for child in node.child if node.child is not None else []:
            node = self.get_node(name, child)
            if node is not None:
                return node

        return None

    def search(self, search_params: SearchParams, node: Node = None, result: List[Node] = None) -> List[Node]:
        node = self.root if node is None else node
        result = [] if result is None else result

        if node.params is not None and search_params.is_satisfies(node.params):
            result.append(node)

        for child in node.child if node.child is not None else []:
            self.search(search_params, child, result)

        return result

