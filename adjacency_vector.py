from generic_structure import GraphStructure

class AdjacencyVector(GraphStructure):
    def __init__(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            node_count = int(f.readline().strip())
            self.adjacency_vector = [[] for _ in range(node_count)]

            for line in f.readlines():
                nodes = line.strip().split()
                if len(nodes) == 2:
                    node_1 = int(nodes[0]) - 1
                    node_2 = int(nodes[1]) - 1
                    self.add_edge(node_1, node_2)

    def add_edge(self, node_1: int, node_2: int):
        self.validate_node_index(node_1, node_2)
        if node_1 == node_2:
            raise ValueError('Self-edges are not allowed.')
        if node_2 not in self.adjacency_vector[node_1]:
            self.adjacency_vector[node_1].append(node_2)
            self.adjacency_vector[node_2].append(node_1)

    def get_node_count(self) -> int:
        return len(self.adjacency_vector)

    def get_neighbors(self, node: int) -> list[int]:
        self.validate_node_index(node)
        return self.adjacency_vector[node]