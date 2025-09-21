from .generic_structure import GraphStructure

class AdjacencyMatrix(GraphStructure):
    def __init__(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as f:
                node_count = int(f.readline().strip())
                self.adjacency_matrix = [
                    [0] * (node_count + 1)
                    for _ in range(node_count + 1)
                ]

                for line in f.readlines():
                    nodes = line.strip().split()
                    if len(nodes) == 2:
                        self.add_edge(int(nodes[0]), int(nodes[1]))
        except MemoryError as e:
            print(f"Não foi possível criar a matriz de adjacência devido à memória insuficiente: {e}")
            raise e

    def add_edge(self, node_1: int, node_2: int) -> None:
        self.validate_node_index(node_1, node_2)
        self.adjacency_matrix[node_1][node_2] = 1
        self.adjacency_matrix[node_2][node_1] = 1

    def get_node_count(self) -> int:
        return len(self.adjacency_matrix) - 1
    
    def get_neighbors(self, node: int) -> list[int]:
        self.validate_node_index(node)
        return [i for i, is_neighbor in enumerate(self.adjacency_matrix[node]) if is_neighbor]