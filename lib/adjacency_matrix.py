from .generic_structure import GraphStructure

class AdjacencyMatrix(GraphStructure):
    def __init__(self, file_path: str, is_directed: bool, reverse: bool = False) -> None:
        self._is_directed = is_directed
        try:
            self._has_negative_weight = False
            with open(file_path, 'r') as f:
                node_count = int(f.readline().strip())
                self.adjacency_matrix = [
                    [''] * (node_count + 1)
                    for _ in range(node_count + 1)
                ]

                for line in f.readlines():
                    nodes = line.strip().split()
                    if len(nodes) == 2:
                        nodes.append('1.0')
                    if reverse:
                        nodes[0], nodes[1] = nodes[1], nodes[0]
                    self.add_edge(int(nodes[0]), int(nodes[1]), float(nodes[2]))
                    if not is_directed:
                        self.add_edge(int(nodes[1]), int(nodes[0]), float(nodes[2]))
        except MemoryError as e:
            print(f"Não foi possível criar a matriz de adjacência devido à memória insuficiente: {e}")
            raise e

    def add_edge(self, node_1: int, node_2: int, weight: float) -> None:
        self.validate_node_index(node_1, node_2)
        if weight < 0:
            self._has_negative_weight = True
        self.adjacency_matrix[node_1][node_2] = weight

    @property
    def is_directed(self) -> bool:
        return self._is_directed

    @property
    def has_negative_weight(self) -> bool:
        return self._has_negative_weight
    
    def get_node_count(self) -> int:
        return len(self.adjacency_matrix) - 1

    def get_neighbors(self, node: int) -> list[tuple[int, float]]:
        self.validate_node_index(node)
        return [(i, weight) for i, weight in enumerate(self.adjacency_matrix[node]) if weight != '']