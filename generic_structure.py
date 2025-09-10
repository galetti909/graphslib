from abc import ABC, abstractmethod

class GraphStructure(ABC):
    @abstractmethod
    def __init__(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_edge_count(self) -> int:
        pass

    @abstractmethod
    def get_node_count(self) -> int:
        pass

    @abstractmethod
    def get_min_degree(self) -> int:
        pass

    @abstractmethod
    def get_max_degree(self) -> int:
        pass

    @abstractmethod
    def get_average_degree(self) -> float:
        pass

    @abstractmethod
    def get_median_degree(self) -> float:
        pass

    @abstractmethod
    def search_breadth_first(self, start_node: int) -> list[tuple[int, int]]:
        pass

    @abstractmethod
    def search_depth_first(self, start_node: int) -> list[tuple[int, int]]:
        pass

    @abstractmethod
    def get_distance(self, node_1: int, node_2: int) -> int:
        pass

    @abstractmethod
    def get_diameter(self) -> int:
        pass

    @abstractmethod
    def list_connected_components(self) -> tuple[int, list[list[int]]]:
        pass

    def __str__(self):
        connected_components = self.list_connected_components()
        connected_components_text = '\n'.join([f'Nodes size: {len(comp)}, {comp}' for comp in connected_components[1]])
        return f'Node count: {self.get_node_count()}\n' \
               f'Edge count: {self.get_edge_count()}\n' \
               f'Min degree: {self.get_min_degree()}\n' \
               f'Max degree: {self.get_max_degree()}\n' \
               f'Average degree: {self.get_average_degree()}\n' \
               f'Median degree: {self.get_median_degree()}\n' \
               f'Connected components count: {connected_components[0]}, organized as:\n{connected_components_text}'