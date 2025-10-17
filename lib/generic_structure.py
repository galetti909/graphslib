# lib/generic_structure.py
from abc import ABC, abstractmethod
import math
from .custom_heap import IndexedMinHeap

class GraphStructure(ABC):
    # --- Métodos abstratos e básicos (init, add_edge, etc.) ---
    @abstractmethod
    def __init__(self, file_path: str) -> None: pass
    @abstractmethod
    def add_edge(self, node_1: int, node_2: int, weight: float): pass
    @abstractmethod
    def get_neighbors(self, node: int) -> list[tuple[int, float]]: pass
    @abstractmethod
    def get_node_count(self) -> int: pass
    @abstractmethod
    def has_negative_weight(self) -> bool: pass

    def validate_node_index(self, *nodes: int) -> None:
        node_count = self.get_node_count()
        for node in nodes:
            if not (1 <= node <= node_count):
                raise ValueError(f'Node index {node} out of bounds (valid: 1 to {node_count}).')
    
    def reconstruct_path(self, prev: list[int | None], start_node: int, end_node: int) -> list[int]:
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            if curr == start_node: break
            curr = prev[curr]
        return path[::-1] if path and path[-1] == start_node else []

    # --- A ÚNICA FUNÇÃO PÚBLICA DE DIJKSTRA ---
    def dijkstra(self, start_node: int, method: str = 'heap') -> tuple[list[float], list[int | None]]:
        """
        Executa o algoritmo de Dijkstra usando a melhor estratégia disponível.

        Args:
            start_node: O vértice de partida.
            method: A implementação a ser usada: 'vector' para a versão O(V^2) 
                    ou 'heap' para a versão otimizada com O(E log V).
        """
        if self.has_negative_weight():
            raise ValueError("O grafo possui pesos negativos. Dijkstra não pode ser aplicado.")

        # O despachante: escolhe a estratégia correta.
        if method == 'vector':
            return self._dijkstra_with_vector(start_node)
        elif method == 'heap':
            # A estratégia 'heap' agora usa a sua implementação superior por padrão.
            return self._dijkstra_with_custom_heap(start_node)
        else:
            raise ValueError(f"Método desconhecido: '{method}'. Use 'vector' ou 'heap'.")

    # --- IMPLEMENTAÇÕES INTERNAS (PRIVADAS) ---

    def _dijkstra_with_vector(self, start_node: int) -> tuple[list[float], list[int | None]]:
        """Estratégia de Dijkstra usando uma lista (O(V^2))."""
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
        """Estratégia de Dijkstra usando o heap personalizado com decrease_key (O(E log V))."""
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