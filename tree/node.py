from tree.node_params import NodeParams
from typing import Dict


class Node:
    name: str = None
    parent = None
    child = None
    params: NodeParams = None

    def __init__(self, json: Dict, parent=None):
        if "name" in json:
            self.name = json["name"]
        else:
            raise ValueError("No name field in json-object")

        self.parent = parent

        if "child" in json and "params" not in json:
            self.child = []
            for obj in json["child"]:
                self.child.append(Node(obj, self))
        elif "params" in json and "child" not in json:
            self.params = NodeParams(json["params"]["max_storage_capacity"],
                                     json["params"]["release_year"],
                                     json["params"]["max_speed"],
                                     json["params"]["average_cost"],
                                     json["params"]["is_general_purpose"],
                                     json["params"]["memory_types"])
        else:
            raise ValueError()

    def __str__(self) -> str:
        return f"\nНаименование: {self.name}\n" + str(self.params)
