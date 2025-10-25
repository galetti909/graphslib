from abc import ABC, abstractmethod

class GenericDijkstraStructuresManager(ABC):
    @abstractmethod
    def __init__(self, n: int) -> None: ...

    @abstractmethod
    def stop(self) -> bool: ...

    @abstractmethod
    def get_next_min(self) -> tuple[int, float]: ...

    @abstractmethod
    def update_distance(self, current_node: int, current_distance: int, node: int, weight: float) -> None: ...

    @abstractmethod
    def result(self) -> list[float]: ...