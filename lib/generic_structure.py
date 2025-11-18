from abc import ABC, abstractmethod
from collections import deque
from typing import Type
from lib.classes.dijkstra.dijkstra_heap import DijkstraHeap
from lib.classes.dijkstra.generic_dijkstra_structures_manager import GenericDijkstraStructuresManager


class GraphStructure(ABC):
    @abstractmethod
    def __init__(self, file_path: str, is_directed: bool) -> None:
        '''Initializes the graph structure from a text file.'''
        pass

    @property
    @abstractmethod
    def is_directed(self) -> bool:
        '''Indicates whether the graph is directed.'''
        pass

    @property
    @abstractmethod
    def has_negative_weight(self) -> bool:
        '''Indicates whether the graph contains any negative weight edges.'''
        pass

    @abstractmethod
    def get_out_neighbors(self, node: int) -> list[int]:
        '''Returns the list of neighboring nodes for the given node.'''
        pass

    @abstractmethod
    def get_node_count(self) -> int:
        '''Returns the total number of nodes in the graph.'''
        pass

    def validate_node_index(self, *nodes: int) -> None:
        '''Validates that the given node indices are within the valid range.'''
        node_count = self.get_node_count()
        for node in nodes:
            if not (1 <= node <= node_count):
                raise ValueError(f'Node index {node} out of bounds for graph with {node_count} nodes (valid indices are 1 to {node_count}).')

    def get_edge_count(self) -> int:
        '''Returns the total number of edges in the graph.'''
        return sum(len(self.get_out_neighbors(node)) for node in range(1, self.get_node_count() + 1)) // (1 if self.is_directed else 2)

    def get_min_out_degree(self) -> int:
        '''Returns the minimum out degree of any node in the graph.'''
        return min(len(self.get_out_neighbors(node)) for node in range(1, self.get_node_count() + 1))

    def get_max_out_degree(self) -> int:
        '''Returns the maximum out degree of any node in the graph.'''
        if self.is_directed:
            raise NotImplementedError('Maximum degree calculation is not implemented for directed graphs.')
        return max(len(self.get_out_neighbors(node)) for node in range(1, self.get_node_count() + 1))

    def get_average_out_degree(self) -> float:
        '''Returns the average out degree of nodes in the graph.'''
        node_count = self.get_node_count()
        if node_count == 0:
            return 0.0
        return sum(len(self.get_out_neighbors(node)) for node in range(1, node_count + 1)) / node_count

    def get_median_out_degree(self) -> float:
        '''Returns the median out degree of nodes in the graph.'''
        node_count = self.get_node_count()
        if node_count == 0:
            return 0.0
        sorted_degrees = sorted(len(self.get_out_neighbors(node)) for node in range(1, node_count + 1))
        mid_index = node_count // 2
        if node_count % 2 == 0:
            return (sorted_degrees[mid_index - 1] + sorted_degrees[mid_index]) / 2
        return float(sorted_degrees[mid_index])

    def search_breadth_first(self, start_node: int, text_file_path: str = '') -> list[tuple[int | None, int | None]]:
        '''Performs a breadth-first search (BFS) starting from the given node.'''
        self.validate_node_index(start_node)
        node_count = self.get_node_count()
        visited: list[tuple[int | None, int | None]] = [(None, None) for _ in range(node_count + 1)]
        visited[start_node] = (None, 0)

        queue = deque([start_node])
        while queue:
            current_node = queue.popleft()
            for neighbor_index, _ in self.get_out_neighbors(current_node):
                if visited[neighbor_index][1] is None:
                    visited[neighbor_index] = (current_node, visited[current_node][1] + 1)
                    queue.append(neighbor_index)
        
        if text_file_path:
            with open(text_file_path, 'w') as f:
                f.write('Node\tParent\tDepth\n')
                for index, (parent, depth) in enumerate(visited[1:]):
                    f.write(f'{index}\t{parent}\t{depth}\n')
        return visited

    def search_depth_first(self, start_node: int, text_file_path: str = '') -> list[tuple[int | None, int | None]]:
        '''Performs a depth-first search (DFS) starting from the given node.'''
        self.validate_node_index(start_node)
        node_count = self.get_node_count()
        visited = [(None, None) for _ in range(node_count + 1)]

        stack = deque([(start_node, None, 0)])
        while stack:
            current_node, parent, depth = stack.pop()
            if visited[current_node][1] is not None:
                continue
            
            visited[current_node] = (parent, depth)
            
            for neighbor_index, _ in sorted(self.get_out_neighbors(current_node), reverse=True):
                if visited[neighbor_index][1] is None:
                    stack.append((neighbor_index, current_node, depth + 1))

        if text_file_path:
            with open(text_file_path, 'w') as f:
                f.write('Node\tParent\tDepth\n')
                for index, (parent, depth) in enumerate(visited[1:]):
                    f.write(f'{index}\t{parent}\t{depth}\n')
        return visited

    def get_edge_distance(self, node_1: int, node_2: int) -> int | None:
        '''Returns the shortest distance in edges between two nodes, or None if unreachable.'''
        self.validate_node_index(node_2)
        bfs_result = self.search_breadth_first(node_1)
        return bfs_result[node_2][1]

    def get_edge_diameter(self) -> int | None:
        '''Returns the diameter, considering distance in edges, of the graph, or None if the graph is disconnected.'''
        if self.get_node_count() <= 1:
            return None
            
        bfs_from_zero = self.search_breadth_first(1)
        depths = [depth for _, depth in bfs_from_zero[1:]]
        if None in depths:
            return None 

        farthest_node_from_zero = depths.index(max(depths)) + 1
        bfs_from_farthest = self.search_breadth_first(farthest_node_from_zero)
        
        final_depths = [depth for _, depth in bfs_from_farthest[1:]]
        return max(final_depths)

    def list_connected_components(self) -> tuple[int, list[list[int]]]:
        '''Returns the number of connected components and a list of lists with their nodes.'''
        components: list[list[int]] = []
        node_count = self.get_node_count()
        visited_nodes = set()

        for i in range(1, node_count + 1):
            if i not in visited_nodes:
                component = []
                bfs_result = self.search_breadth_first(i)
                for index, (_, depth) in enumerate(bfs_result):
                    if depth is not None:
                        visited_nodes.add(index)
                        component.append(index)
                components.append(component)

        components.sort(key=len, reverse=True)
        return len(components), components

    def get_all_distances_and_fathers_from_start_node(self, start_node: int, queue_type: Type[GenericDijkstraStructuresManager] = DijkstraHeap) -> list[tuple[float, int | None]]:
        '''Given a start node, returns the distance to all other nodes, and its father through best path'''
        if self.has_negative_weight:
            raise ValueError('Graph contains negative weight edges; Dijkstra\'s algorithm cannot be applied. Algorithms for negative weights not implemented yet.')
        dijkstra_manager = queue_type(start_node, self.get_node_count())
        while next := dijkstra_manager.get_next_min():
            current_node, current_distance = next
            for neighbor, weight in self.get_out_neighbors(current_node):
                dijkstra_manager.update_distance(current_node, current_distance, neighbor, weight)
        return dijkstra_manager.result()
    
    def get_all_distances_and_sons_to_end_node(self, end_node: int) -> list[tuple[float, int | None]]:
        '''Given an end node, returns the distance from all other nodes, and its sons through best path'''
        self.validate_node_index(end_node)
        node_count = self.get_node_count()
        distances_and_sons: list[tuple[float, int | None]] = [(float('inf'), None) for _ in range(node_count + 1)]
        distances_and_sons[end_node] = (0.0, None)
        converged = False
        for i in range(1, node_count):
            print('i', i)
            if converged:
                break
            converged = True
            for node in range(1, node_count + 1):
                for neighbor, weight in self.get_out_neighbors(node):
                    if (new_value := round(distances_and_sons[neighbor][0] + weight, 2)) < distances_and_sons[node][0]:
                        distances_and_sons[node] = (new_value, neighbor)
                        converged = False
        else:
            for node in range(1, node_count + 1):
                for neighbor, weight in self.get_out_neighbors(node):
                        if round(distances_and_sons[neighbor][0] + weight, 2) < distances_and_sons[node][0]:
                            raise ValueError('Graph contains a negative weight cycle; shortest paths not well-defined.')
        return distances_and_sons

    def generate_graph_text_file(self, file_path: str) -> None:
        '''Generates a text file representation of the graph's properties.'''
        with open(file_path, 'w') as f:
            f.write(str(self))

    def __str__(self) -> str:
        count, components = self.list_connected_components()
        comp_text_list = []
        for comp in components:
            comp_text_list.append(f'  - Componente com {len(comp)} vértices: {comp}')

        connected_components_text = '\n'.join(comp_text_list)
        
        return (
            f'Número de Vértices: {self.get_node_count()}\n'
            f'Número de Arestas: {self.get_edge_count()}\n'
            f'Grau de Saída Mínimo: {self.get_min_out_degree()}\n'
            f'Grau de Saída Máximo: {self.get_max_out_degree()}\n'
            f'Grau de Saída Médio: {self.get_average_out_degree():.2f}\n'
            f'Mediana de Grau de Saída: {self.get_median_out_degree()}\n'
            f'Componentes Conexas: {count}\n{connected_components_text}'
        )