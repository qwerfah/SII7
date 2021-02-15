from enums.memory_type import MemoryType

from functools import reduce
from typing import List


class NodeParams:
    def __init__(self,
                 capacity: float,
                 release_year: int,
                 max_speed: float,
                 average_cost: float,
                 is_general_purpose: bool,
                 memory_types: List[MemoryType]):
        if capacity < 0:
            raise ValueError("Емкость не омжет быть олтрицательной")
        if release_year < 0 or release_year > 2020:
            raise ValueError("Год выпуска не может быть отрицательным")
        if average_cost < 0:
            raise ValueError("Стоимость не ожет быть отрицательной")

        self.capacity: float = capacity
        self.release_year: int = release_year
        self.max_speed: float = max_speed
        self.average_cost: float = average_cost
        self.is_general_purpose: bool = is_general_purpose
        self.memory_types: List[MemoryType] = []

        for memory_type in memory_types:
            if memory_type == 0:
                self.memory_types.append(MemoryType.RAM)
            elif memory_type == 1:
                self.memory_types.append(MemoryType.GRAPHIC_MEMORY)
            elif memory_type == 2:
                self.memory_types.append(MemoryType.MICRO_RAM)
            elif memory_type == 3:
                self.memory_types.append(MemoryType.CACHE_MEMORY)
            elif memory_type == 4:
                self.memory_types.append(MemoryType.SECONDARY_MEMORY)

    def __str__(self) -> str:
        purpose: str = "Вторичная память" if self.is_general_purpose else "Первичная память"
        types: str = reduce(lambda res, memory_type: res + "; " + memory_type.value, self.memory_types, "")

        return f"Максимальная емкость накопителя, Мб: {self.capacity}\n" + \
            f"Максимальная скорость, Мб/с: {self.max_speed}\n" + \
            f"Средняя стоимость, Руб/Мб: {self.average_cost}\n" + \
            f"Год выпуска: {self.release_year}\n" + \
            f"Назначение: {purpose}\n" + \
            f"Типы: {types}\n"
