from lib import AdjacencyVector
import time
import random

def distances_to_100(graph: AdjacencyVector, end_node: int) -> int:
    distances = graph.get_all_distances_and_sons_to_end_node(end_node)
    return (distances[10][0], distances[20][0], distances[30][0])

def average_execution_time(graph: AdjacencyVector) -> float:
    total_time = 0
    runs = 5
    n = graph.get_node_count()
    for node in random.sample(range(1, n + 1), runs):
        start_time = time.perf_counter()
        graph.get_all_distances_and_sons_to_end_node(node)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    return total_time / runs

def dijkstra_distances_to_100(graph: AdjacencyVector, end_node: int) -> int:
    distances = graph.get_all_distances_and_fathers_from_start_node(end_node)
    return (distances[10][0], distances[20][0], distances[30][0])

def average_execution_time(graph: AdjacencyVector) -> float:
    total_time = 0
    runs = 5
    n = graph.get_node_count()
    for node in random.sample(range(1, n + 1), runs):
        start_time = time.perf_counter()
        graph.get_all_distances_and_sons_to_end_node(node)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    return total_time / runs