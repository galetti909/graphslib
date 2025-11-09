import time
import random
from typing import Type
from lib import GraphStructure
from lib.classes.dijkstra.dijkstra_heap import DijkstraHeap
from lib.classes.dijkstra.dijkstra_vector import DijkstraVector
from lib.classes.dijkstra.generic_dijkstra_structures_manager import GenericDijkstraStructuresManager

def case_1_min_distances(graph: GraphStructure, start_node: int) -> list[float]:
    return graph.get_all_distances_and_fathers_from_start_node(start_node)

def case_2_dijkstra_performance_comparison(graph: GraphStructure) -> tuple[float, float]:
    def measure_dijkstra_time(queue_type: Type[GenericDijkstraStructuresManager]) -> float:
        total_time = 0
        n = graph.get_node_count()
        for start_node in random.sample(range(1, n + 1), 5):
            start_time = time.perf_counter()
            graph.get_all_distances_and_fathers_from_start_node(start_node, queue_type)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        return total_time / 5
    avg_time_vector = measure_dijkstra_time(DijkstraVector)
    avg_time_heap = measure_dijkstra_time(DijkstraHeap)
    return avg_time_vector, avg_time_heap

def case_3_distance_between_researchers(graph: GraphStructure, researchers_names_file_path: str, start_researcher: str, end_researchers: list[str]) -> list[dict[str, tuple[float, str]]]:
    end_researchers_indexes = []
    researchers_names = ['']
    
    with open(researchers_names_file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            i = line[0]
            name = line[1]
            researchers_names.append(name.strip())
            if start_researcher == name:
                start_researcher_index = int(i)
            if name in end_researchers:
                end_researchers_indexes.append(int(i))

    if not start_researcher_index:
        raise ValueError(f'Start researcher "{start_researcher}" not found in researchers names file.')
    distances_and_fathers = graph.get_all_distances_and_fathers_from_start_node(start_researcher_index)

    print(end_researchers_indexes)
    return [
        {
            researchers_names[end]: (
                distances_and_fathers[end][0],
                researchers_names[distances_and_fathers[end][1]] if distances_and_fathers[end][1] is not None else None
            )
        }
        for end in end_researchers_indexes
    ]