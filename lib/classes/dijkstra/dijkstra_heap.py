import heapq
from lib.classes.dijkstra.generic_dijkstra_structures_manager import GenericDijkstraStructuresManager

class DijkstraHeap(GenericDijkstraStructuresManager):
    def __init__(self, start_node: int, n: int) -> None:
        self.distances_and_fathers = [(float('inf'), None)] * n
        self.distances_and_fathers[start_node] = (0, None)
        self.visited_size = 0
        self.graph_size = n
        self.min_heap = []

    def stop(self) -> bool:
        return self.visited_size == self.graph_size

    def get_next_min(self) -> tuple[float, int]:
        while True:
            dist, father, node = heapq.heappop(self.min_heap)
            if self.distances_and_fathers[node][0] == float('inf'):
                self.distances_and_fathers[node] = (dist, father)
                self.visited_size += 1
                return node, dist

    def update_distance(self, current_node: int, current_distance: int, node: int, weight: float) -> None:
        if self.distances_and_fathers[node][0] != float('inf'):
            return
        heapq.heappush(self.min_heap, (current_distance + weight, current_node, node))

    def result(self) -> list[float]:
        return self.distances_and_fathers
