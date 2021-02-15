from tree.node import Node
from typing import Dict, List
from functools import reduce

from dialog_system.search_params import SearchParams
from dialog_system.utilities import Utilities


class Tree:
    """ Дерево данных. """

    root: Node

    def __init__(self, json: Dict):
        if "root" in json:
            self.root = Node(json["root"])
        else:
            raise ValueError("No root in json-object")

    def get_node(self, name: str, node: Node = None) -> Node:
        """ Возвращает узел дерева по имени. """

        node = self.root if node is None else node
        name = name.lower()
        node_name: str = reduce(lambda res, word: res + word, Utilities.parse(node.name), "")
        if node_name == name:
            return node

        for child in node.child if node.child is not None else []:
            node = self.get_node(name, child)
            if node is not None:
                return node

        return None

    def to_list(self, node: Node = None, nodes: List[Node] = None) -> List[Node]:
        """ Записывает в список все листья дерева начиная от указанного корневого узла. """

        node = self.root if node is None else node
        nodes = [] if nodes is None else nodes

        if node.child is None or node.child == []:
            nodes.append(node)
        else:
            for child in node.child if node.child is not None else []:
                self.to_list(child, nodes)

        return nodes

    def search(self, search_params: SearchParams, node: Node = None, result: List[Node] = None) -> List[Node]:
        """ Ищет в дереве все узлы, удовлетворяющие
            параметрам поиска, и возвращает их в виде списка. """

        node = self.root if node is None else node
        result = [] if result is None else result

        if node.params is not None and search_params.is_satisfies(node.params):
            result.append(node)

        for child in node.child if node.child is not None else []:
            self.search(search_params, child, result)

        return result

