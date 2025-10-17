# lib/generic_structure.py
from abc import ABC, abstractmethod
import math
from .custom_heap import IndexedMinHeap

class GraphStructure(ABC):
    # Abstract methods to be implemented by subclasses. 
    @abstractmethod
    def __init__(self, file_path: str) -> None:
        # Initializes the graph from a file.
        pass

    @abstractmethod
    def add_edge(self, node_1: int, node_2: int, weight: float):
        # Adds a weighted edge between two nodes.
        pass

    @abstractmethod
    def get_neighbors(self, node: int) -> list[tuple[int, float]]:
        # Returns a list of (neighbor, weight) tuples for a node.
        pass
    
    @abstractmethod
    def get_node_count(self) -> int:
        # Returns the total number of nodes in the graph.
        pass

    @abstractmethod
    def has_negative_weight(self) -> bool:
        # Checks if the graph contains any negative edge weights.
        pass

    # --- Concrete methods available to all subclasses ---
    def validate_node_index(self, *nodes: int) -> None:
        # Validates if node indices are within the graph's bounds.
        node_count = self.get_node_count()
        for node in nodes:
            if not (1 <= node <= node_count):
                raise ValueError(f'Node index {node} out of bounds (valid: 1 to {node_count}).')
    
    def reconstruct_path(self, prev: list[int | None], start_node: int, end_node: int) -> list[int]:
        # Reconstructs the shortest path from Dijkstra's predecessors array.
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            if curr == start_node: break
            curr = prev[curr]
        return path[::-1] if path and path[-1] == start_node else []

    # --- Main public Dijkstra's algorithm interface ---
    def dijkstra(self, start_node: int, method: str = 'heap') -> tuple[list[float], list[int | None]]:
        """
        Executes Dijkstra's algorithm using a specified strategy.
        'heap' method uses the efficient custom heap, 'vector' uses the simple list.
        """
        if self.has_negative_weight():
            raise ValueError("Dijkstra cannot be applied to graphs with negative weights.")

        # Dispatcher: chooses the correct internal implementation based on the method.
        if method == 'vector':
            return self._dijkstra_with_vector(start_node)
        elif method == 'heap':
            return self._dijkstra_with_custom_heap(start_node)
        else:
            raise ValueError(f"Unknown method: '{method}'. Use 'vector' or 'heap'.")

    # --- Internal (private) implementations for Dijkstra's ---

    def _dijkstra_with_vector(self, start_node: int) -> tuple[list[float], list[int | None]]:
        # Dijkstra's strategy using a list to find the minimum distance node (O(V^2)).
        node_count = self.get_node_count()
        dist = [math.inf] * (node_count + 1)
        prev = [None] * (node_count + 1)
        dist[start_node] = 0
        unvisited = list(range(1, node_count + 1))
        while unvisited:
            u = min(unvisited, key=lambda node: dist[node])
            if dist[u] == math.inf: break
            unvisited.remove(u)
            for v, weight in self.get_neighbors(u):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
        return dist, prev

    def _dijkstra_with_custom_heap(self, start_node: int) -> tuple[list[float], list[int | None]]:
        # Dijkstra's strategy using a custom indexed heap with decrease_key (O(E log V)).
        node_count = self.get_node_count()
        dist = [math.inf] * (node_count + 1)
        prev = [None] * (node_count + 1)
        dist[start_node] = 0
        pq = IndexedMinHeap()
        for i in range(1, node_count + 1):
            pq.push(i, dist[i])
        while not pq.is_empty():
            distance, u = pq.pop_min()
            if distance == math.inf: break
            for v, weight in self.get_neighbors(u):
                if v in pq:
                    new_dist = dist[u] + weight
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = u
                        pq.decrease_key(v, new_dist)
        return dist, prev