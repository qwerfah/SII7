from tree.memory_type import MemoryType
from typing import List


class NodeParams:
    def __init__(self,
                 max_storage_capacity: float,
                 release_year: int,
                 max_speed: float,
                 average_cost: float,
                 is_general_purpose: bool,
                 memory_types: List[MemoryType]):
        if max_storage_capacity < 0:
            raise ValueError("Емкость не омжет быть олтрицательной")
        if release_year < 0 or release_year > 2020:
            raise ValueError("Год выпуска не может быть отрицательным")
        if average_cost < 0:
            raise ValueError("Стоимость не ожет быть отрицательной")

        self.max_storage_capacity: float = max_storage_capacity
        self.release_year: int = release_year
        self.max_speed: float = max_speed
        self.average_cost: float = average_cost
        self.is_general_purpose: bool = is_general_purpose
        self.memory_types: List[MemoryType] = memory_types
