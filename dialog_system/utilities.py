from typing import List, Dict, Callable, Tuple
import pymorphy2
import string


class Utilities:
    analyzer = pymorphy2.MorphAnalyzer()
    translation: Dict[str, str] = str.maketrans(dict.fromkeys(string.punctuation.replace("-", ""), " "))

    @staticmethod
    def parse(message: str) -> List[str]:
        """ Очистить сообщение от знаков препинания, привести
            к нижнему регистру и привести все слова в начальную форму. """

        message: str = message.lower()
        message = message.translate(Utilities.translation)
        words: List[str] = message.split()

        return list(map(lambda word: Utilities.analyzer.parse(word)[0].normal_form, words))

    @staticmethod
    def pairs(lst: List[any]) -> List[Tuple[Tuple[any, int], Tuple[any, int]]]:
        """ Представляет одномерный список в виде списка пар соседних элементов вместе с их индексами. """

        if len(lst) < 2:
            return []

        for i in range(1, len(lst)):
            yield (lst[i - 1], i - 1), (lst[i], i)

    @staticmethod
    def triples(lst: List[any]) -> List[Tuple[Tuple[any, int], Tuple[any, int], Tuple[any, int]]]:
        """ Представляет одномерный список в виде списка троек соседних элементов вместе с их индексами. """

        if len(lst) < 3:
            return []

        for i in range(2, len(lst)):
            yield (lst[i - 2], i - 2), (lst[i - 1], i - 1), (lst[i], i)

