# lib/generic_structure.py
from abc import ABC, abstractmethod
import math
import heapq
from .custom_heap import IndexedMinHeap

class GraphStructure(ABC):
    @abstractmethod
    def __init__(self, file_path: str) -> None:
        pass

    @abstractmethod
    def add_edge(self, node_1: int, node_2: int, weight: float):
        pass

    @abstractmethod
    def get_neighbors(self, node: int) -> list[tuple[int, float]]:
        pass
    
    @abstractmethod
    def get_node_count(self) -> int:
        pass

    @abstractmethod
    def has_negative_weight(self) -> bool:
        pass

    def validate_node_index(self, *nodes: int) -> None:
        node_count = self.get_node_count()
        for node in nodes:
            if not (1 <= node <= node_count):
                raise ValueError(f'Node index {node} out of bounds (valid: 1 to {node_count}).')
    
    def reconstruct_path(self, prev: list[int | None], start_node: int, end_node: int) -> list[int]:
        # Reconstructs the shortest path from the predecessors array.
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            if curr == start_node:
                break
            curr = prev[curr]
        
        return path[::-1] if path and path[-1] == start_node else []

    def dijkstra_with_vector(self, start_node: int) -> tuple[list[float], list[int | None]]:
        # Dijkstra's algorithm using a list to find the minimum distance node.
        if self.has_negative_weight():
            raise ValueError("Dijkstra cannot be applied to graphs with negative weights.")
        
        node_count = self.get_node_count()
        dist = [math.inf] * (node_count + 1)
        prev = [None] * (node_count + 1)
        dist[start_node] = 0
        
        unvisited = list(range(1, node_count + 1))

        while unvisited:
            # Slow operation: find the minimum in the entire list
            u = min(unvisited, key=lambda node: dist[node])
            if dist[u] == math.inf:
                break
            unvisited.remove(u)

            for v, weight in self.get_neighbors(u):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
        
        return dist, prev

    def dijkstra_with_heap(self, start_node: int) -> tuple[list[float], list[int | None]]:
        """Dijkstra's algorithm using Python's standard heapq library (lazy deletion)."""
        if self.has_negative_weight():
            raise ValueError("Dijkstra cannot be applied to graphs with negative weights.")

        node_count = self.get_node_count()
        dist = [math.inf] * (node_count + 1)
        prev = [None] * (node_count + 1)
        dist[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue # Ignore obsolete entries

            for v, weight in self.get_neighbors(u):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        return dist, prev

    def dijkstra_with_custom_heap(self, start_node: int) -> tuple[list[float], list[int | None]]:
        """Dijkstra's algorithm using a custom heap with an efficient decrease_key operation."""
        if self.has_negative_weight():
            raise ValueError("Dijkstra cannot be applied to graphs with negative weights.")

        node_count = self.get_node_count()
        dist = [math.inf] * (node_count + 1)
        prev = [None] * (node_count + 1)
        dist[start_node] = 0

        pq = IndexedMinHeap()
        for i in range(1, node_count + 1):
            pq.push(i, dist[i])

        while not pq.is_empty():
            distance, u = pq.pop_min()
            if distance == math.inf:
                break

            for v, weight in self.get_neighbors(u):
                if v in pq:
                    new_dist = dist[u] + weight
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = u
                        pq.decrease_key(v, new_dist)
        
        return dist, prev