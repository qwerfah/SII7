from tree.memory_type import MemoryType
from tree.node_params import NodeParams

from typing import List, Tuple


class SearchParams:
    def __init__(self,
                 capacity_range: (float, float) = None,
                 year_range: (int, int) = None,
                 speed_range: (float, float) = None,
                 cost_range: (float, float) = None,
                 is_general_purpose: bool = None,
                 memory_type: MemoryType = None):
        if capacity_range is not None and (capacity_range[0] < 0 or capacity_range[1] < 0):
            raise ValueError("Емкость не омжет быть олтрицательной.")
        if year_range is not None and (year_range[0] < 0 or year_range[1] < 0):
            raise ValueError("Год выпуска не может быть отрицательным.")
        if cost_range is not None and (cost_range[0] < 0 or cost_range[1] < 0):
            raise ValueError("Стоимость не ожет быть отрицательной.")

        if capacity_range is not None and capacity_range[0] > capacity_range[1]:
            raise ValueError("Нижняя граница числового интервала не может быть больше верхней.")
        if year_range is not None and year_range[0] > year_range[1]:
            raise ValueError("Нижняя граница числового интервала не может быть больше верхней.")
        if cost_range is not None and cost_range[0] > cost_range[1]:
            raise ValueError("Нижняя граница числового интервала не может быть больше верхней.")

        self.capacity_range: (float, float) = capacity_range
        self.year_range: (int, int) = year_range
        self.speed_range: (float, float) = speed_range
        self.cost_range: (float, float) = cost_range
        self.purpose: bool = is_general_purpose
        self.memory_type: MemoryType = memory_type

    @staticmethod
    def is_in_range(value: float, value_range: Tuple[float, float]) -> bool:
        if value_range is None or (value_range[0] is None and value_range[1] is None):
            return True
        elif value_range[0] is not None and value_range[1] is None and value >= value_range[0]:
            return True
        elif value_range[0] is None and value_range[1] is not None and value <= value_range[1]:
            return True
        elif value_range[0] is not None and value_range[1] is not None and value_range[0] <= value <= value_range[1]:
            return True
        return False

    def is_satisfies(self, node_params: NodeParams) -> bool:
        points: int = 0

        points += 1 if SearchParams.is_in_range(node_params.max_storage_capacity, self.capacity_range) else 0
        points += 1 if SearchParams.is_in_range(node_params.max_speed, self.speed_range) else 0
        points += 1 if SearchParams.is_in_range(node_params.release_year, self.year_range) else 0
        points += 1 if SearchParams.is_in_range(node_params.average_cost, self.cost_range) else 0
        points += 1 if self.purpose is None or self.purpose == node_params.is_general_purpose else 0
        if self.memory_type is None:
            points += 1
        else:
            try:
                node_params.memory_types.index(self.memory_type)
                points += 1
            except ValueError:
                pass

        return points == 6
