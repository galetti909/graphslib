from generic_structure import GraphStructure

class AdjacencyVector(GraphStructure):
    def __init__(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            self.adjacency_vector = [[]] * int(f.readline().strip())

            for line in f.readlines():
                nodes = line.strip().split()
                if len(nodes) == 2: 
                    self.add_edge(int(nodes[0]), int(nodes[1]))

    def add_edge(self, node_1: int, node_2: int):
        self.validate_node_index(node_1, node_2)
        if node_1 == node_2:
            raise ValueError('Self-edges are not allowed.')
        self.adjacency_vector[node_1] += [node_2]
        self.adjacency_vector[node_2] += [node_1]

    def get_node_count(self) -> int:
        return len(self.adjacency_vector)

    def get_neighbors(self, node: int) -> list[int]:
        self.validate_node_index(node)
        return self.adjacency_vector[node]