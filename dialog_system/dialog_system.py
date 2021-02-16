from tree.tree import Tree
from enums.action_type import ActionType
from dialog_system.params_extractor import ParamsExtractor
from dialog_system.search_params import SearchParams
from tree.node import Node
import dialog_system.resources as resources
from dialog_system.utilities import Utilities

from typing import List, Dict, Callable, Tuple
from prettytable import PrettyTable
from functools import reduce
from accessify import private
import json
import random


class DialogSystem:
    """ Диалоговая система, использующая pymorphy и дерево данных,
     загружаемое из json-файла. """

    tree: Tree
    params_extractor: ParamsExtractor = ParamsExtractor()

    def __init__(self, tree: Tree = None):
        if tree is not None:
            self.tree = tree
        else:
            with open("./resources/tree.json", "r",  encoding="utf-8") as json_file:
                self.tree = Tree(json.load(json_file))

    def answer(self, message: str) -> str:
        """ Сформировать ответ на пользовательский запрос. """

        words: List[str] = Utilities.parse(message)
        print(words)
        actions: List[ActionType] = list(map(lambda pair: resources.action_synonyms.get(
            pair[0][0] + pair[1][0], ActionType.Unknown), Utilities.pairs(words)))

        actions += list(map(lambda word: resources.action_synonyms.get(word, ActionType.Unknown), words))
        actions = sorted(actions, key=lambda act: act.value, reverse=False)
        action_type: ActionType = actions.pop()
        action: Callable[[List[str]], str] = self.actions.get(action_type)

        return action(self, words)

        try:
            return action(self, words)
        except:
            return self.unknown(words)

    @private
    def help(self, words: List[str]) -> str:
        """ Вывод справочной информации о системе. """

        return resources.help_message

    @private
    def search(self, words: List[str]) -> str:
        """ Поиск на основе указанны пользователем параметров. """

        nodes: List[Node] = []

        search_params: SearchParams = self.params_extractor.extract_params_by_words(words)

        random.seed()

        if search_params is None:
            nodes = self.extract_nodes_by_names(words)

            print(nodes)

            if nodes is None or nodes == []:
                try:
                    words.index("все")
                    nodes = self.tree.to_list()
                except ValueError:
                    try:
                        words.index("всё")
                        nodes = self.tree.to_list()
                    except ValueError:
                        return resources.cant_found_messages[random.randint(0, len(resources.cant_found_messages) - 1)]
        else:
            print("Capacity: ", search_params.capacity_range)
            print("Speed: ", search_params.speed_range)
            print("Cost: ", search_params.cost_range)
            print("Year: ", search_params.year_range)
            print("Purpose: ", search_params.purpose)
            print("Type:", search_params.memory_type)

            nodes = self.tree.search(search_params)

            if nodes is None or nodes == []:
                return resources.not_found_messages[random.randint(0, len(resources.not_found_messages) - 1)]

        return resources.found_messages[random.randint(0, len(resources.found_messages) - 1)] + \
            reduce(lambda res, n: res + str(n), nodes, "")

    @private
    def compare(self, words: List[str]) -> str:
        """ Сравнение двух указанных типов памяти.
            (если указано больше двух, рассматриваются только первые два) """

        i: int = 0
        nodes: List[Node] = self.extract_nodes_by_names(words)
        random.seed()

        if len(nodes) < 2:
            return resources.cant_compare_messages[random.randint(0, len(resources.cant_compare_messages) - 1)]

        table: PrettyTable = PrettyTable([
            "Наименование",
            "Емкость",
            "Скорость",
            "Стоимость",
            "Год выпуска",
            "Назначение",
            "Тип"
        ])

        for node in nodes:
            table.add_row([
                node.name,
                node.params.capacity,
                node.params.max_speed,
                node.params.average_cost,
                node.params.release_year,
                "Вторичная память" if node.params.is_general_purpose else "Первичная память",
                reduce(lambda res, s: res + " " + s.value, node.params.memory_types, "")
            ])

        result: PrettyTable = PrettyTable([
            "Наиболее вместительный",
            "Самый быстрый",
            "Самый дешевый",
            "Самый новый"
        ])

        result.add_row([
            reduce(lambda a, b: a if a.params.capacity > b.params.capacity else b, list(nodes), list(nodes)[0]).name,
            reduce(lambda a, b: a if a.params.max_speed > b.params.max_speed else b, list(nodes), list(nodes)[0]).name,
            reduce(lambda a, b: a if a.params.average_cost < b.params.average_cost else b, list(nodes), list(nodes)[0]).name,
            reduce(lambda a, b: a if a.params.release_year > b.params.release_year else b, list(nodes), list(nodes)[0]).name
        ])

        return resources.compare_messages[random.randint(0, len(resources.compare_messages) - 1)] + str(table) + "\n" + str(result)

    @private
    def unknown(self, words: List[str]) -> str:
        """ Выполняется в случае, когда запрашиваемое
            пользователем действие не удалось определить. """

        random.seed()
        return resources.unknown_messages[random.randint(0, len(resources.unknown_messages) - 1)]

    @private
    def exit(self, words: List[str]) -> str:
        """ Завершение работы системы. """

        random.seed()
        return resources.exit_messages[random.randint(0, len(resources.exit_messages) - 1)]

    @private
    def extract_nodes_by_names(self, words: List[str]) -> List[Node]:
        """ Ищет в строке все возможные имена узлов дерева
            по тройкам, парам слов и просто по словам. """

        nodes: List[Node] = []
        del_offset: int = 0
        triples: List[Tuple[Tuple[any, int], Tuple[any, int], Tuple[any, int]]] = list(Utilities.triples(words))

        for triple in triples:
            node: Node = self.tree.get_node(triple[0][0] + triple[1][0] + triple[2][0])
            if node is not None:
                del words[triple[0][1] - del_offset]
                del words[triple[1][1] - del_offset - 1]
                del words[triple[2][1] - del_offset - 2]
                nodes += self.tree.to_list(node)
                del_offset += 3

        pairs: List[Tuple[Tuple[any, int], Tuple[any, int]]] = list(Utilities.pairs(words))
        del_offset = 0

        for pair in pairs:
            node: Node = self.tree.get_node(pair[0][0] + pair[1][0])
            if node is not None:
                del words[pair[0][1] - del_offset]
                del words[pair[1][1] - del_offset - 1]
                nodes += self.tree.to_list(node)
                del_offset += 2

        for word in words:
            node: Node = self.tree.get_node(word)
            if node is not None:
                nodes += self.tree.to_list(node)

        return list(dict.fromkeys(nodes))

    """ Словарь действий (каждому типу действия сопоставлена функция, реализующая это действие). """
    actions: Dict[ActionType, Callable[[List[str]], str]] = {
        ActionType.Unknown: unknown,
        ActionType.Help: help,
        ActionType.Search: search,
        ActionType.Comparison: compare,
        ActionType.Exit: exit,
    }
