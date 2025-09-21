import os
import time

from psutil import Process

from lib import GraphStructure

def case_1_memory_analysis(graph: GraphStructure) -> float:
    process = Process(os.getpid())
    mem_usage = process.memory_info().rss / (1024 * 1024)
    return mem_usage

def cases_2_3_bfs_dfs_performance(graph: GraphStructure, start_nodes: list[int]) -> tuple[float,float]:
    def measure_search_time(search_function):
        total_time = 0
        for start_node in start_nodes:
            start_time = time.perf_counter()
            search_function(start_node)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        return total_time / len(start_nodes)

    bfs_avg_time = measure_search_time(graph.search_breadth_first)
    dfs_avg_time = measure_search_time(graph.search_depth_first)
    return bfs_avg_time, dfs_avg_time

def case_4_parents_in_search_trees(graph: GraphStructure, start_vertice: int, targets: int) -> tuple[int | None, int | None]:
    bfs = graph.search_breadth_first(start_vertice)
    dfs = graph.search_depth_first(start_vertice)
    bfs_parents = [bfs[target][0] for target in targets]
    dfs_parents = [dfs[target][0] for target in targets]
    return bfs_parents, dfs_parents

def case_5_distance_between_vertices(graph: GraphStructure, node_1: int, node_2: int) -> int | None:
    return graph.get_distance(node_1, node_2)

def case_6_connected_components(graph: GraphStructure) -> tuple[int, list[list[int]]]:
    return graph.list_connected_components()

def case_7_graph_diameter(graph: GraphStructure) -> int | None:
    return graph.get_diameter()


