from .generic_structure import GraphStructure

class AdjacencyVector(GraphStructure):
    def __init__(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            self._has_negative_weight = False
            node_count = int(f.readline().strip())
            self.adjacency_vector = [[] for _ in range(node_count + 1)]

            for line in f.readlines():
                nodes = line.strip().split()
                if len(nodes) == 3:
                    self.add_edge(int(nodes[0]), int(nodes[1]), float(nodes[2]))

    def add_edge(self, node_1: int, node_2: int, weight: float = 1.0) -> None:
        self.validate_node_index(node_1, node_2)
        if weight < 0:
            self._has_negative_weight = True
        if node_2 not in self.adjacency_vector[node_1]:
            self.adjacency_vector[node_1].append((node_2, weight))
            self.adjacency_vector[node_2].append((node_1, weight))

    @property
    def has_negative_weight(self) -> bool:
        return self._has_negative_weight

    def get_node_count(self) -> int:
        return len(self.adjacency_vector) - 1

    def get_neighbors(self, node: int) -> list[tuple[int, float]]:
        self.validate_node_index(node)
        return self.adjacency_vector[node]