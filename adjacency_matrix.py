from collections import deque
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

    def get_edge_count(self) -> int:
        return sum(sum(row) for row in self.adjacency_matrix) / 2
    
    def get_node_count(self) -> int:
        return len(self.adjacency_matrix)

    def get_min_degree(self) -> int:
        return min(sum(row) for row in self.adjacency_matrix)

    def get_max_degree(self) -> int:
        return max(sum(row) for row in self.adjacency_matrix)

    def get_average_degree(self) -> float:
        return sum(sum(row) for row in self.adjacency_matrix) / self.get_node_count()

    def get_median_degree(self) -> float:
        degrees = [sum(row) for row in self.adjacency_matrix]
        degrees.sort()
        if len(degrees) % 2 == 1:
            return degrees[len(degrees) // 2]
        return (degrees[len(degrees) // 2 - 1] + degrees[len(degrees) // 2]) / 2
    
    def search_breadth_first(self, start_node: int) -> list[tuple[int, int]]: # (parent, depth)
        if start_node >= (node_count := self.get_node_count()):
            raise ValueError(f'Node index out of bounds. Last valid index is {node_count - 1}.')
        elif start_node < 0:
            raise ValueError('Node index must be non-negative.')
        
        visited = [(None, None) for _ in range(self.get_node_count())]
        visited[start_node] = (None, 0)  # (parent, depth)

        queue = deque([start_node]) # (node, parent)
        while queue:
            current_node = queue.popleft()
            for neighbor_index, is_connected in enumerate(self.adjacency_matrix[current_node]):
                if is_connected and visited[neighbor_index][1] is None:
                    visited[neighbor_index] = (current_node, visited[current_node][1] + 1)
                    queue.append(neighbor_index)

        return visited
    
    def search_depth_first(self, start_node: int) -> list[tuple[int, int]]: # (parent, depth)
        if start_node >= (node_count := self.get_node_count()):
            raise ValueError(f'Node index out of bounds. Last valid index is {node_count - 1}.')
        elif start_node < 0:
            raise ValueError('Node index must be non-negative.')
        
        visited = [(None, None) for _ in range(self.get_node_count())]

        stack = deque([(start_node, None)]) # (node, parent)
        while stack:
            current_node, current_parent = stack.pop()
            if visited[current_node][1] is not None:
                continue
            visited[current_node] = (current_parent, visited[current_parent][1] + 1 if current_parent is not None else 0)
            for neighbor_index, is_connected in enumerate(self.adjacency_matrix[current_node]):
                if is_connected:
                    stack.append((neighbor_index, current_node))
        return visited
