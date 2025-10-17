# lib/adjacency_matrix.py
from .generic_structure import GraphStructure
import math

class AdjacencyMatrix(GraphStructure):
    def __init__(self, file_path: str) -> None:
        self._has_negative_weight = False
        with open(file_path, 'r') as f:
            lines = f.readlines()
            self.node_count = int(lines[0].strip())
            
            # The matrix now stores weights (floats). 'inf' means no edge.
            self.adjacency_matrix = [[math.inf] * (self.node_count + 1) for _ in range(self.node_count + 1)]
            for i in range(1, self.node_count + 1):
                self.adjacency_matrix[i][i] = 0

            for line in lines[1:]:
                parts = line.strip().split()
                if len(parts) >= 2:
                    node_1 = int(parts[0])
                    node_2 = int(parts[1])
                    # Reads weight from the third column. Defaults to 1.0 if not present.
                    weight = float(parts[2]) if len(parts) > 2 else 1.0
                    self.add_edge(node_1, node_2, weight)

    def has_negative_weight(self) -> bool:
        return self._has_negative_weight

    def add_edge(self, node_1: int, node_2: int, weight: float):
        self.validate_node_index(node_1, node_2)
        if node_1 == node_2: return

        if weight < 0:
            self._has_negative_weight = True

        self.adjacency_matrix[node_1][node_2] = weight
        self.adjacency_matrix[node_2][node_1] = weight

    def get_neighbors(self, node: int) -> list[tuple[int, float]]:
        self.validate_node_index(node)
        neighbors = []
        # Returns (neighbor, weight) for existing edges.
        for i, weight in enumerate(self.adjacency_matrix[node][1:], 1):
            if i != node and weight != math.inf:
                neighbors.append((i, weight))
        return neighbors

    def get_node_count(self) -> int:
        return self.node_count