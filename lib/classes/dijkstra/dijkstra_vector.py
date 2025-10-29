from lib.classes.dijkstra.generic_dijkstra_structures_manager import GenericDijkstraStructuresManager

# Dijkstra's algorithm implementation using a Vector
class DijkstraVector(GenericDijkstraStructuresManager):
    def __init__(self, start_node: int, n: int) -> None:
        self.boundary_set_size = 1 
        self.distances_and_fathers = [(float('inf'), None)] * (n + 1)
        self.distances_and_fathers[start_node] = (0, None)
        self.visited = [False] * (n + 1) 

    def get_next_min(self) -> tuple[float, int] | None:
        if self.boundary_set_size == 0:
            return None
        
        min_dist = float('inf')
        
        for node, (dist, _) in enumerate(self.distances_and_fathers):
            if self.visited[node]:
                continue
            if dist < min_dist:
                min_dist = dist
                min_node = node
        
        self.boundary_set_size -= 1
        self.visited[min_node] = True 
        return min_node, min_dist

    def update_distance(self, current_node: int, current_distance: int, node: int, weight: float) -> None:
        # If neighbor 'node' is already finalized, skip
        if self.visited[node]:
            return
        
        new_distance = round(current_distance + weight, 2)
        old_distance, _ = self.distances_and_fathers[node]
        
        # Standard edge relaxation
        if new_distance < old_distance:
            self.distances_and_fathers[node] = (new_distance, current_node)
            # If we're visiting this node for the first time, add it to the frontier
            if old_distance == float('inf'):
                self.boundary_set_size += 1

    def result(self) -> list[tuple[float, int | None]]:
        return self.distances_and_fathers