from .generic_structure import GraphStructure

class AdjacencyMatrix(GraphStructure):
    def __init__(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as f:
                node_count = int(f.readline().strip())
                self.adjacency_matrix = [
                    [''] * (node_count + 1)
                    for _ in range(node_count + 1)
                ]

                for line in f.readlines():
                    nodes = line.strip().split()
                    if len(nodes) == 3:
                        self.add_edge(int(nodes[0]), int(nodes[1]), float(nodes[2]))
        except MemoryError as e:
            print(f"Não foi possível criar a matriz de adjacência devido à memória insuficiente: {e}")
            raise e

    def add_edge(self, node_1: int, node_2: int, weight: float = 1.0) -> None:
        self.validate_node_index(node_1, node_2)
        if weight < 0:
            self.has_negative_weight = True
        self.adjacency_matrix[node_1][node_2] = weight
        self.adjacency_matrix[node_2][node_1] = weight

    def get_node_count(self) -> int:
        return len(self.adjacency_matrix) - 1

    def get_neighbors(self, node: int) -> list[tuple[int, float]]:
        self.validate_node_index(node)
        return [(i, weight) for i, weight in enumerate(self.adjacency_matrix[node]) if weight != '']