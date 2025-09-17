from abc import ABC, abstractmethod
from collections import deque

class GraphStructure(ABC):
    @abstractmethod
    def __init__(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_neighbors(self, node: int) -> list[int]:
        pass

    @abstractmethod
    def get_node_count(self) -> int:
        pass

    def validate_node_index(self, *nodes: int) -> None:
        node_count = self.get_node_count()
        for node in nodes:
            if not (0 <= node < node_count):
                raise ValueError(f'Node index {node} out of bounds for graph with {node_count} nodes (valid indices are 0 to {node_count - 1}).')

    def get_edge_count(self) -> int:
        return sum(len(self.get_neighbors(node)) for node in range(self.get_node_count())) // 2

    def get_min_degree(self) -> int:
        return min(len(self.get_neighbors(node)) for node in range(self.get_node_count()))

    def get_max_degree(self) -> int:
        return max(len(self.get_neighbors(node)) for node in range(self.get_node_count()))

    def get_average_degree(self) -> float:
        node_count = self.get_node_count()
        if node_count == 0:
            return 0.0
        return sum(len(self.get_neighbors(node)) for node in range(node_count)) / node_count

    def get_median_degree(self) -> float:
        node_count = self.get_node_count()
        if node_count == 0:
            return 0.0
        sorted_degrees = sorted(len(self.get_neighbors(node)) for node in range(node_count))
        mid_index = node_count // 2
        if node_count % 2 == 0:
            return (sorted_degrees[mid_index - 1] + sorted_degrees[mid_index]) / 2
        return float(sorted_degrees[mid_index])

    def search_breadth_first(self, start_node: int, text_file_path: str = '') -> list[tuple[int | None, int | None]]:  # (parent, depth)
        self.validate_node_index(start_node)
        node_count = self.get_node_count()
        visited = [(None, None) for _ in range(node_count)]
        visited[start_node] = (None, 0)

        queue = deque([start_node])
        while queue:
            current_node = queue.popleft()
            for neighbor_index in self.get_neighbors(current_node):
                if visited[neighbor_index][1] is None:
                    visited[neighbor_index] = (current_node, visited[current_node][1] + 1)
                    queue.append(neighbor_index)
        
        if text_file_path:
            with open(text_file_path, 'w') as f:
                f.write('Node\tParent\tDepth\n')
                for index, (parent, depth) in enumerate(visited):
                    parent_display = parent + 1 if parent is not None else 'None'
                    f.write(f'{index + 1}\t{parent_display}\t{depth}\n')
        return visited

    def search_depth_first(self, start_node: int, text_file_path: str = '') -> list[tuple[int | None, int | None]]: # (parent, depth)
        self.validate_node_index(start_node)
        node_count = self.get_node_count()
        visited = [(None, None) for _ in range(node_count)]
        
        stack = deque([(start_node, None, 0)]) # (node, parent, depth)
        while stack:
            current_node, parent, depth = stack.pop()
            if visited[current_node][1] is not None:
                continue
            
            visited[current_node] = (parent, depth)
            
            # add neighbors in reverse order so that DFS explores in ascendig index order
            for neighbor_index in sorted(self.get_neighbors(current_node), reverse=True):
                if visited[neighbor_index][1] is None:
                    stack.append((neighbor_index, current_node, depth + 1))

        if text_file_path:
            with open(text_file_path, 'w') as f:
                f.write('Node\tParent\tDepth\n')
                for index, (parent, depth) in enumerate(visited):
                    parent_display = parent + 1 if parent is not None else 'None'
                    f.write(f'{index + 1}\t{parent_display}\t{depth}\n')
        return visited

    def get_distance(self, node_1: int, node_2: int) -> int | None:
        self.validate_node_index(node_1, node_2)
        bfs_result = self.search_breadth_first(node_1)
        return bfs_result[node_2][1]

    def get_diameter(self) -> int | None:
        if self.get_node_count() <= 1:
            return None
            
        # heuristic 2-BFS to diameter
        bfs_from_zero = self.search_breadth_first(0)
        depths = [depth for _, depth in bfs_from_zero]
        if None in depths: # Grafo desconexo
            return None 

        farthest_node_from_zero = depths.index(max(depths))
        bfs_from_farthest = self.search_breadth_first(farthest_node_from_zero)
        
        final_depths = [depth for _, depth in bfs_from_farthest]
        return max(final_depths)

    def list_connected_components(self) -> tuple[int, list[list[int]]]:
        components: list[list[int]] = []
        node_count = self.get_node_count()
        visited_nodes = set()

        for i in range(node_count):
            if i not in visited_nodes:
                component = []
                bfs_result = self.search_breadth_first(i)
                for index, (parent, depth) in enumerate(bfs_result):
                    if depth is not None:
                        component.append(index)
                        visited_nodes.add(index)
                components.append(component)

        # fix: sort components by size, from largest to smallest
        components.sort(key=len, reverse=True)
        return len(components), components

    def generate_graph_text_file(self, file_path: str) -> None:
        with open(file_path, 'w') as f:
            f.write(str(self))

    def __str__(self) -> str:
        count, components = self.list_connected_components()
        # Converts the nodes to base 1 for display
        comp_text_list = []
        for comp in components:
            comp_display = [node + 1 for node in comp]
            comp_text_list.append(f'  - Componente com {len(comp_display)} vértices: {comp_display}')

        connected_components_text = '\n'.join(comp_text_list)
        
        return (f'Número de Vértices: {self.get_node_count()}\n'
                f'Número de Arestas: {self.get_edge_count()}\n'
                f'Grau Mínimo: {self.get_min_degree()}\n'
                f'Grau Máximo: {self.get_max_degree()}\n'
                f'Grau Médio: {self.get_average_degree():.2f}\n'
                f'Mediana de Grau: {self.get_median_degree()}\n'
                f'Componentes Conexas: {count}\n{connected_components_text}')