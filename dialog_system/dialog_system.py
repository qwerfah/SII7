from tree.tree import Tree
from dialog_system.action_type import ActionType
from dialog_system.params_extractor import ParamsExtractor
from dialog_system.search_params import SearchParams
import dialog_system.resources as resources

from typing import List, Dict, Callable, Tuple
from accessify import private
import pymorphy2
import json
import string
import random


class DialogSystem:
    """ Диалоговая система, использующая pymorphy и дерево данных,
     загружаемое из json-файла. """

    tree: Tree
    analyzer = pymorphy2.MorphAnalyzer()
    params_extractor: ParamsExtractor = ParamsExtractor()
    translation: Dict[str, str] = str.maketrans(dict.fromkeys(string.punctuation.replace("-", ""), " "))

    def __init__(self, tree: Tree = None):
        if tree is not None:
            self.tree = tree
        else:
            with open("./resources/tree.json", "r") as json_file:
                self.tree = Tree(json.load(json_file))

    def answer(self, message: str) -> str:
        words: List[str] = self.parse(message)
        actions: List[ActionType] = list(map(lambda pair: resources.action_synonyms.get(
            pair[0] + pair[1], ActionType.Unknown), self.pairs(words)))
        # print(actions)

        actions += list(map(lambda word: resources.action_synonyms.get(word, ActionType.Unknown), words))
        # print(actions)

        actions = sorted(actions, key=lambda act: act.value, reverse=False)
        # print(actions)

        action_type: ActionType = actions.pop()
        action: Callable[[], str] = self.actions.get(action_type)

        if action_type == ActionType.Search:
            params: SearchParams = self.params_extractor.extract_params_by_words(words)
            # print(params)
            return action(self, params)

        return action(self)

    @private
    def clean_message(self, message: str) -> str:
        message: str = message.lower()
        message: str = message.translate(self.translation)

        return message

    @private
    def parse(self, message: str) -> List[str]:
        message: str = self.clean_message(message)
        words: List[str] = message.split()

        return list(map(lambda word: self.analyzer.parse(word)[0].normal_form, words))

    @private
    def pairs(self, lst: List[any]) -> List[Tuple[any, any]]:
        for i in range(1, len(lst)):
            yield lst[i - 1], lst[i]

    @private
    def help(self) -> str:
        return "Помощь"

    @private
    def search(self, params: SearchParams) -> str:
        print(params.capacity_range)
        print(params.speed_range)
        print(params.cost_range)
        print(params.year_range)
        print(params.purpose)
        print(params.memory_types)

    @private
    def unknown(self) -> str:
        random.seed()
        return resources.unknown_messages[random.randint(0, len(resources.unknown_messages) - 1)]

    @private
    def exit(self) -> str:
        return "Завершение работы..."

    actions: Dict[ActionType, Callable[[], str]] = {
        ActionType.Help: help,
        ActionType.Search: search,
        ActionType.Exit: exit,
        ActionType.Unknown: unknown
    }
