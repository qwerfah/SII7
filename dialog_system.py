from tree.tree import Tree
from action_type import ActionType
from param_type import ParamType
from tree.node_params import NodeParams

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

    action_synonyms: Dict[str, ParamType] = {
        "помощь": ActionType.Help,
        "помочь": ActionType.Help,
        "уметь": ActionType.Help,
        "мочь": ActionType.Help,
        "подсказать": ActionType.Help,

        "найти": ActionType.Search,
        "отыскать": ActionType.Search,
        "искать": ActionType.Search,
        "поиск": ActionType.Search,
        "подобрать": ActionType.Search,
        "нужный": ActionType.Search,
        "необходимый": ActionType.Search,
        "требоваться": ActionType.Search,
        "показать": ActionType.Search,
        "отобразить": ActionType.Search,
        "помочьнайти": ActionType.Search,
        "помочьотыскать": ActionType.Search,
        "подобрать": ActionType.Search,
        "помочьподобрать": ActionType.Search,


        "выйти": ActionType.Exit,
        "завершить": ActionType.Exit,
        "выход": ActionType.Exit,
        "стоп": ActionType.Exit,
    }

    param_synonyms: Dict[str, ParamType] = {
        "объем": ParamType.Capacity,
        "емкость": ParamType.Capacity,
        "размер": ParamType.Capacity,
        "вместительность": ParamType.Capacity,

        "скорость": ParamType.Speed,

        "год": ParamType.Year,
        "годвыпуск": ParamType.Year,
        "годрелиз": ParamType.Year,

        "стоимость": ParamType.Cost,
        "цена": ParamType.Cost,

        "назначение": ParamType.Purpose,

        "тип": ParamType.Types,
    }

    unknown_messages: List[str] = [
        "Извините, не понял вас. Попробуйте задать другой вопрос.",
        "Простите, я вас не понимаю. Попытайтесь сформулировать запрос иначе.",
        "Прошу прощения, я вас не понимаю, повторите запрос.",
        "Ничего не понял, попробуйте спросить что-то другое.",
        "Не смог найти ответ на ваш вопрос, может что-то еще?",
        "Не нашел ни одного подходящего варианта ответа, спросите еще раз.",
        "Простите, я не настолько умный, не знаю что вам ответить.",
        "В if-else нет варианта, подходящего под ваш запрос (искусственный интеллект слишком искусственный)."
    ]

    def __init__(self, tree: Tree = None):
        if tree is not None:
            self.tree = tree
        else:
            with open("./resources/tree.json", "r") as json_file:
                self.tree = Tree(json.load(json_file))

    def answer(self, message: str) -> str:
        words: List[str] = self.parse(message)
        actions: List[ActionType] = list(map(lambda pair: self.action_synonyms.get(
            pair[0] + pair[1], ActionType.Unknown), self.pairs(words)))
        print(actions)
        actions = list(map(lambda word: self.action_synonyms.get(word, ActionType.Unknown), words))
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
        return self.unknown_messages[random.randint(0, len(self.unknown_messages) - 1)]

    @private
    def exit(self):
        return "Завершение работы..."

    actions: Dict[ActionType, Callable[[], str]] = {
        ActionType.Help: help,
        ActionType.Search: search,
        ActionType.Exit: exit,
        ActionType.Unknown: unknown
    }

