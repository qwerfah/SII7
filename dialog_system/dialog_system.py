from tree.tree import Tree
from dialog_system.action_type import ActionType
from tree.node_params import NodeParams
import dialog_system.resources as resources

from typing import List, Dict, Callable
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
        print(actions)
        actions = list(map(lambda word: resources.action_synonyms.get(word, ActionType.Unknown), words))
        print(actions)
        actions = sorted(actions, key=lambda act: act.value, reverse=False)
        print(actions)
        action = self.actions.get(actions.pop())
        print(action)

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
    def extract_param(self, message: str): pass

    @private
    def extract_params(self, words: List[str]):
        params: NodeParams = NodeParams()

        for w1, w2 in self.pairs(words): pass

    @private
    def pairs(self, lst: List[any]):
        for i in range(1, len(lst)):
            yield lst[i - 1], lst[i]

    @private
    def help(self) -> str:
        return "Помощь"

    @private
    def search(self) -> str: pass

    @private
    def unknown(self) -> str:
        random.seed()
        return resources.unknown_messages[random.randint(0, len(resources.unknown_messages) - 1)]

    @private
    def exit(self):
        return "Завершение работы..."

    actions: Dict[ActionType, Callable[[], str]] = {
        ActionType.Help: help,
        ActionType.Search: search,
        ActionType.Exit: exit,
        ActionType.Unknown: unknown
    }

