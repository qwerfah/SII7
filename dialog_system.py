from tree.tree import Tree
from action_type import ActionType
from typing import List, Dict, Callable
import pymorphy2
import json
import string


class DialogSystem:
    """ Диалоговая система, использующая pymorphy и дерево данных,
     загружаемое из json-файла. """

    tree: Tree
    analyzer = pymorphy2.MorphAnalyzer()
    translation: Dict[str, str] = str.maketrans(dict.fromkeys(string.punctuation.replace("-", ""), " "))

    synonyms = {
        "помощь": ActionType.Help,
        "помочь": ActionType.Help,
        "уметь": ActionType.Help,
        "мочь": ActionType.Help,
        "подсказать": ActionType.Help,

        "найти": ActionType.Search,
        "искать": ActionType.Search,
        "поиск": ActionType.Search,
        "подобрать": ActionType.Search,
        "нужный": ActionType.Search,
        "показать": ActionType.Search,
        "отобразить": ActionType.Search,
    }

    def __init__(self, tree: Tree = None):
        if tree is not None:
            self.tree = tree
        else:
            with open("./resources/tree.json", "r") as json_file:
                self.tree = Tree(json.load(json_file))

    def clean_message(self, message: str) -> str:
        message: str = message.lower()
        message: str = message.translate(self.translation)

        return message

    def parse(self, message: str) -> List[str]:
        message: str = self.clean_message(message)
        words: List[str] = message.split()

        return list(map(lambda word: self.analyzer.parse(word)[0].normal_form, words))

    def answer(self, message: str) -> str:
        words: List[str] = self.parse(message)
        actions: List[ActionType] = list(map(lambda word: self.synonyms.get(word, ActionType.Unknown), words))
        actions = [action for action in actions if action != ActionType.Unknown]
        actions = sorted(actions, key=lambda action: action.value, reverse=True)

    def help(self) -> str: pass
    def search(self) -> str: pass
    def unknown(self) -> str: pass

    actions: Dict[ActionType, Callable[[], str]] = {
        ActionType.Help: help,
        ActionType.Search: search,
        ActionType.Unknown: unknown
    }

