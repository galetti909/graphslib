from generic_structure import GraphStructure

class AdjacencyMatrix(GraphStructure):
    def __init__(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            self.adjacency_matrix = [
                [0] * (node_count := int(f.readline().strip())) 
                for _ in range(node_count)
            ]

            for line in f.readlines():
                nodes = line.strip().split()
                if len(nodes) == 2: 
                    self.add_edge(int(nodes[0]), int(nodes[1]))

    def add_edge(self, node_1: int, node_2: int):
        if node_1 >= (node_count := self.get_node_count()) or node_2 >= node_count:
            raise ValueError(f'Node index out of bounds. Last valid index is {node_count - 1}.')
        elif node_1 < 0 or node_2 < 0:
            raise ValueError('Node index must be non-negative.')
        elif node_1 == node_2:
            raise ValueError('Self-edges are not allowed.')
        self.adjacency_matrix[node_1][node_2] = 1
        self.adjacency_matrix[node_2][node_1] = 1