from tree.node import Node
from typing import Dict


class Tree:
    root: Node

    def __init__(self, json: Dict):
        if "root" in json:
            self.root = Node(json["root"])
        else:
            raise ValueError("No root in json-object")
