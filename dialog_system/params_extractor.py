from accessify import private
from typing import List, Tuple, Dict, Union
from functools import reduce
from enum import Enum

from dialog_system.search_params import SearchParams
from enums.param_type import ParamType
import dialog_system.resources as resources


class ParamsExtractor:
    """ Предоставляет методы для извлечения поддерживаемого
        системой набора параметров из пользовательского запроса. """

    def extract_params_by_words(self, words: List[str]) -> SearchParams:
        """ Извлекает из строки, представленной списком слов, все
            поддерживаемые параметры в интервалах между ключевыми
            словами, исходя из предположения, что между двумя
            ключевыми словами не может быть больше двух значений параметров. """

        prev_idx: int = 0
        curr_idx: int = 0
        next_idx: int = 0

        print(words)

        n: int = len(words)
        param_types: List[ParamType] = []
        param_values: List[Tuple[float, float]] = []

        for i in range(n + 1):
            if i < n:
                param_type: ParamType = resources.param_synonyms.get(words[i], ParamType.Unknown)
                if param_type != ParamType.Unknown:
                    param_types.append(param_type)
            if param_type != ParamType.Unknown or i == n:
                prev_idx, curr_idx, next_idx = curr_idx, next_idx, i
                if prev_idx != curr_idx:
                    param_values += self.extract_param_between(words, prev_idx, curr_idx)

        param_values += self.extract_param_between(words, curr_idx, next_idx)

        return self.pack_params(param_types, param_values)

    @private
    def try_get_index(self, words: List[str], synonyms: List[str]) -> int:
        """ Пытыется определить индекс первого вхождения любого из элементов списка 
            synonyms в список words. Если ни один из них не содержится в words, возвращает None. """

        for symonym in synonyms:
            try:
                return words.index(symonym)
            except ValueError:
                continue
        
        return None

    @private
    def extract_num_param(self, words: List[str]) -> Tuple[float, float]:
        """ Извлекает из указанного набора слов первый
            числовой параметр в виде диапазона или скалярного значения. """

        """ Сначала в виде диапазона <a-b> """
        ranges: Dict[Tuple[int, ...], Tuple[float, float]] = {}

        try:
            ind: int = words.index("-")
            value_range: Tuple[float, float] = float(words[ind - 1]), float(words[ind + 1])
            ranges.update({(ind - 1, ind, ind + 1): value_range})
        except ValueError:
            pass

        for i in range(len(words)):
            try:
                value_range = list(map(float, words[i].split('-')))
                if len(value_range) == 2:
                    ranges.update({tuple([i]): value_range})
            except ValueError:
                pass

        """ Затем в виде диапазона <от a до b>.
            Сначала ищем нижнюю границу диапазона. """
        value_range: Tuple[float, float] = (None, None)
        from_ind: int = self.try_get_index(words, resources.from_synonyms)
        if from_ind is not None:
            value_range = float(words[from_ind + 1]), None
            ranges.update({(from_ind, from_ind + 1): value_range})

        """ Затем ищем верхнюю границу диапазона. """
        to_ind: int = self.try_get_index(words, resources.to_synonyms)
        if to_ind is not None:
            value_range = value_range[0], float(words[to_ind + 1])
            if from_ind is not None and to_ind >= from_ind and value_range[0] <= value_range[1]:
                del ranges[(from_ind, from_ind + 1)]
                ranges.update({(from_ind, from_ind + 1, to_ind, to_ind + 1): value_range})
            else:
                ranges.update({(to_ind, to_ind + 1): value_range})

        """ Если ранее ничего не было найдено, ищем в виде скалярного значения. """
        for i in set(range(len(words))) - set(reduce(lambda lst, el: lst + el, ranges, ())):
            try:
                value = float(words[i])
                ranges.update({tuple([i]): (value, value)})
                break
            except ValueError:
                pass

        """ Выбираем первое из всех найденных значений (если их было несколько). """
        min_el: Tuple[int, ...] = tuple([len(words)])
        for elem in ranges:
            if elem[0] <= min_el[0]:
                min_el = elem

        """ Удаляем найденное значение из исходного набора слов и возвращаем в качестве результата """
        try:
            diff: int = 0
            for i in set(min_el) - {len(words)}:
                del words[i - diff]
                diff += 1

            return ranges[min_el]
        except:
            return None

    @private
    def extract_bool_param(self, words: List[str]) -> bool:
        """ Извлекает из указанного набора слов первый логический
            параметр на основе соответствующего словаря синонимов. """

        for i in range(len(words)):
            try:
                value: bool = resources.purpose_synonyms[words[i]]
                del words[i]
                return value
            except KeyError:
                pass

        return None

    @private
    def extract_enum_param(self, words: List[str]) -> Enum:
        """ Извлекает из указанного набора слов первый перечислимый
            параметр на основе соответствующего словаря синонимов. """

        for i in range(len(words)):
            try:
                value: Enum = resources.type_synonyms[words[i]]
                del words[i]
                return value
            except KeyError:
                pass

        return None


    @private
    def extract_param_between(self, words: List[str], from_word: int, to_word: int) \
            -> List[Union[Tuple[float, float], bool, Enum]]:
        """ Извлекает из указанного интервала входного
            набора слов все поддерживаемые виды параметров. """

        sub_words: List[str] = words[from_word: to_word]
        values: List[Union[Tuple[float, float], bool, Enum]] = []

        """ Извлекаем сначала числовые параметры """
        for j in range(2):
            value_range: Tuple[float, float] = self.extract_num_param(sub_words)
            if value_range is not None:
                values.append(value_range)

        """ Затем извлекаем параметры логического типа (назначение) """
        bool_param: bool = self.extract_bool_param(sub_words)
        if bool_param is not None:
            values.append(bool_param)

        """ В конце извлекаем перечислимые параметры """
        enum_param: Enum = self.extract_enum_param(sub_words)
        if enum_param is not None:
            values.append(enum_param)

        return values

    @private
    def pack_params(self, param_types: List[ParamType],
                    param_values: List[Union[Tuple[float, float], bool, Enum]]) -> SearchParams:
        """ Упаковывает все найденные параметры в объект класса SearchParams. """

        """ Если для значений параметров не были указаны ключевые 
            слова, предугадываем известные типы параметров """
        for i in range(len(param_values)):
            if isinstance(param_values[i], bool):
                try:
                    param_types.index(ParamType.Purpose)
                except ValueError:
                    param_types.insert(i, ParamType.Purpose)
            elif isinstance(param_values[i], Enum):
                try:
                    param_types.index(ParamType.Types)
                except ValueError:
                    param_types.insert(i, ParamType.Types)

        print(param_types)
        print(param_values)

        n: int = len(param_types) if len(param_types) <= len(param_values) else len(param_values)
        if n == 0:
            return None

        search_params: SearchParams = SearchParams()

        for i in range(n):
            if param_types[i] == ParamType.Capacity:
                search_params.capacity_range = param_values[i]
            elif param_types[i] == ParamType.Speed:
                search_params.speed_range = param_values[i]
            elif param_types[i] == ParamType.Cost:
                search_params.cost_range = param_values[i]
            elif param_types[i] == ParamType.Year:
                search_params.year_range = param_values[i]
            elif param_types[i] == ParamType.Purpose:
                search_params.purpose = param_values[i]
            elif param_types[i] == ParamType.Types:
                search_params.memory_type = param_values[i]

        return search_params
