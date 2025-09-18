from .generic_structure import GraphStructure
from .utils import decrement_entry_nodes_index

class AdjacencyMatrix(GraphStructure):
    def __init__(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            node_count = int(f.readline().strip())
            self.adjacency_matrix = [
                [0] * node_count 
                for _ in range(node_count)
            ]

            for line in f.readlines():
                nodes = line.strip().split()
                if len(nodes) == 2:
                    # fix: adjust indexing to 0
                    self.add_edge(int(nodes[0]), int(nodes[1]))

    def add_edge(self, node_1: int, node_2: int):
        node_1 = decrement_entry_nodes_index(node_1)
        node_2 = decrement_entry_nodes_index(node_2)
        self.validate_node_index(node_1, node_2)
        if node_1 == node_2:
            raise ValueError('Self-edges are not allowed.')
        self.adjacency_matrix[node_1][node_2] = 1
        self.adjacency_matrix[node_2][node_1] = 1
    
    def get_node_count(self) -> int:
        return len(self.adjacency_matrix)
    
    def _get_neighbors(self, node: int) -> list[int]: # Private method to avoid nodes index confusion
        self.validate_node_index(node)
        return [i for i, is_neighbor in enumerate(self.adjacency_matrix[node]) if is_neighbor]