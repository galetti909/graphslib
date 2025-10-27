import heapq
from lib.classes.dijkstra.generic_dijkstra_structures_manager import GenericDijkstraStructuresManager

class DijkstraHeap(GenericDijkstraStructuresManager):
    def __init__(self, start_node: int, n: int) -> None:
        self.distances_and_fathers = [(float('inf'), None)] * (n + 1)
        self.min_heap = [(0, None, start_node)]

    def get_next_min(self) -> tuple[float, int] | None:
        while True:
            if not self.min_heap:
                return None
            dist, father, node = heapq.heappop(self.min_heap)
            if self.distances_and_fathers[node][0] == float('inf'):
                self.distances_and_fathers[node] = (dist, father)
                return node, dist

    def update_distance(self, current_node: int, current_distance: int, node: int, weight: float) -> None:
        if self.distances_and_fathers[node][0] != float('inf'):
            return
        heapq.heappush(self.min_heap, (round(current_distance + weight, 2), current_node, node))

    def result(self) -> list[float]:
        return self.distances_and_fathers
