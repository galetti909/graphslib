from abc import ABC, abstractmethod
from collections import deque

class GraphStructure(ABC):
    @abstractmethod
    def __init__(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_neighbors(self, node: int) -> list[int]:
        pass

    @abstractmethod
    def get_node_count(self) -> int:
        pass

    def get_edge_count(self) -> int:
        return sum(len(self.get_neighbors(node)) for node in range(self.get_node_count())) / 2

    def get_min_degree(self) -> int:
        return min(len(self.get_neighbors(node)) for node in range(self.get_node_count()))

    def get_max_degree(self) -> int:
        return max(len(self.get_neighbors(node)) for node in range(self.get_node_count()))

    def get_average_degree(self) -> float:
        node_count = self.get_node_count()
        return sum(len(self.get_neighbors(node)) for node in range(node_count)) / node_count

    def get_median_degree(self) -> float:
        node_count = self.get_node_count()
        sorted_degrees = sorted(len(self.get_neighbors(node)) for node in range(node_count))
        mid_index = node_count // 2
        if node_count % 2 == 0:
            return (sorted_degrees[mid_index - 1] + sorted_degrees[mid_index]) / 2
        return sorted_degrees[mid_index]

    def search_breadth_first(self, start_node: int) -> list[tuple[int, int]]: # (parent, depth)
        if start_node >= (node_count := self.get_node_count()):
            raise ValueError(f'Node index out of bounds. Last valid index is {node_count - 1}.')
        elif start_node < 0:
            raise ValueError('Node index must be non-negative.')
        
        visited = [(None, None) for _ in range(self.get_node_count())]
        visited[start_node] = (None, 0)  # (parent, depth)

        queue = deque([start_node]) # (node, parent)
        while queue:
            current_node = queue.popleft()
            for neighbor_index in self.get_neighbors(current_node):
                if visited[neighbor_index][1] is None:
                    visited[neighbor_index] = (current_node, visited[current_node][1] + 1)
                    queue.append(neighbor_index)
        return visited

    def search_depth_first(self, start_node: int) -> list[tuple[int, int]]: # (parent, depth)
        if start_node >= (node_count := self.get_node_count()):
            raise ValueError(f'Node index out of bounds. Last valid index is {node_count - 1}.')
        elif start_node < 0:
            raise ValueError('Node index must be non-negative.')
        
        visited = [(None, None) for _ in range(self.get_node_count())]

        stack = deque([(start_node, None)]) # (node, parent)
        while stack:
            current_node, current_parent = stack.pop()
            if visited[current_node][1] is not None:
                continue
            visited[current_node] = (current_parent, visited[current_parent][1] + 1 if current_parent is not None else 0)
            for neighbor_index in self.get_neighbors(current_node):
                stack.append((neighbor_index, current_node))
        return visited

    def get_distance(self, node_1: int, node_2: int) -> int | None:
        if node_1 >= (node_count := self.get_node_count()) or node_2 >= node_count:
            raise ValueError(f'Node index out of bounds. Last valid index is {node_count - 1}.')
        elif node_1 < 0 or node_2 < 0:
            raise ValueError('Node index must be non-negative.')
        
        bfs_result = self.search_breadth_first(node_1)
        return bfs_result[node_2][1] if bfs_result[node_2][1] is not None else None

    def get_diameter(self) -> int | None:
        bfs_from_first = self.search_breadth_first(0)
        depths = [depth for _, depth in bfs_from_first]
        if None in depths:
            return None # Graph is disconnected
        farthest_node = depths.index(max(depths))

        bfs_from_farthest = self.search_breadth_first(farthest_node)
        return max(depth for _, depth in bfs_from_farthest)

    def list_connected_components(self) -> tuple[int, list[list[int]]]:
        components: list[list[int]] = []
        node_count = self.get_node_count()
        nodes = set(range(node_count))
        while sum(len(component) for component in components) < node_count:
            current_node = next(nodes - set(sum(components, start=[])))
            bfs_result = self.search_breadth_first(current_node)
            component = [index for index, (_, depth) in enumerate(bfs_result) if depth is not None]
            components.append(component)
        return len(components), components

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