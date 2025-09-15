import time
import random
import os
import psutil
from adjacency_matrix import AdjacencyMatrix
from adjacency_vector import AdjacencyVector
from generic_structure import GraphStructure

def run_case_study(graph_file_path: str):
    """
    Executes the case study for a given graph file,
    analyzing the adjacency matrix and vector representations.
    """
    if not os.path.exists(graph_file_path):
        print(f"ERROR: Graph file not found at '{graph_file_path}'")
        return

    print("=" * 60)
    print(f"Starting Case Study for Graph: {graph_file_path}")
    print("=" * 60)

    # --- Case Study 1: Memory Analysis ---
    print("\n[Analysis 1: Memory Usage]")
    process = psutil.Process(os.getpid())

    # Adjacency Matrix
    graph_matrix = AdjacencyMatrix(graph_file_path)
    mem_matrix = process.memory_info().rss / (1024 * 1024)
    print(f"Memory used (Adjacency Matrix): {mem_matrix:.4f} MB")
    node_count = graph_matrix.get_node_count()
    del graph_matrix

    # Adjacency Vector
    graph_vector = AdjacencyVector(graph_file_path)
    mem_vector = process.memory_info().rss / (1024 * 1024)
    print(f"Memory used (Adjacency Vector): {mem_vector:.4f} MB")
    del graph_vector
    
    # --- Case Studies 2 & 3: BFS and DFS Performance ---
    print("\n[Analysis 2 and 3: Search Performance (Average Time)]")
    num_runs = min(100, node_count)
    start_nodes = random.sample(range(node_count), num_runs) if num_runs > 0 else []

    def measure_search_time(search_function, graph_instance):
        total_time = 0
        if not start_nodes: return 0
        for start_node in start_nodes:
            start_time = time.perf_counter()
            search_function(start_node)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        return total_time / num_runs

    # Measuring for Adjacency Matrix
    graph_matrix_perf = AdjacencyMatrix(graph_file_path)
    bfs_matrix_avg_time = measure_search_time(graph_matrix_perf.search_breadth_first, graph_matrix_perf)
    dfs_matrix_avg_time = measure_search_time(graph_matrix_perf.search_depth_first, graph_matrix_perf)
    print(f"Average BFS Time (Matrix): {bfs_matrix_avg_time:.8f} seconds")
    print(f"Average DFS Time (Matrix): {dfs_matrix_avg_time:.8f} seconds")
    del graph_matrix_perf

    # Measuring for Adjacency Vector
    graph_vector_perf = AdjacencyVector(graph_file_path)
    bfs_vector_avg_time = measure_search_time(graph_vector_perf.search_breadth_first, graph_vector_perf)
    dfs_vector_avg_time = measure_search_time(graph_vector_perf.search_depth_first, graph_vector_perf)
    print(f"Average BFS Time (Vector): {bfs_vector_avg_time:.8f} seconds")
    print(f"Average DFS Time (Vector): {dfs_vector_avg_time:.8f} seconds")

    # --- Detailed Analyses (using Adjacency Vector) ---
    graph = graph_vector_perf 
    print("\n--- Detailed Analyses (using Adjacency Vector) ---")

    # --- Case Study 4: Parents of Vertices in Search Trees ---
    print("\n[Analysis 4: Parents of Vertices in Search Trees]")
    start_vertices = [1, 2, 3]
    target_vertices = [10, 20, 30]
    
    for start_v in start_vertices:
        start_v_idx = start_v - 1
        if 0 <= start_v_idx < node_count:
            bfs_tree = graph.search_breadth_first(start_v_idx)
            dfs_tree = graph.search_depth_first(start_v_idx)
            print(f"\n> Searches starting from vertex {start_v}:")
            for target_v in target_vertices:
                target_v_idx = target_v - 1
                if 0 <= target_v_idx < node_count:
                    parent_bfs = bfs_tree[target_v_idx][0]
                    parent_bfs_display = parent_bfs + 1 if parent_bfs is not None else "None"
                    parent_dfs = dfs_tree[target_v_idx][0]
                    parent_dfs_display = parent_dfs + 1 if parent_dfs is not None else "None"
                    print(f"  - Vertex {target_v}: Parent in BFS = {parent_bfs_display}, Parent in DFS = {parent_dfs_display}")

    # --- Case Study 5: Distances Between Pairs of Vertices ---
    print("\n[Analysis 5: Distances Between Pairs of Vertices]")
    pairs = [(10, 20), (10, 30), (20, 30)]
    for v1, v2 in pairs:
        v1_idx, v2_idx = v1 - 1, v2 - 1
        if (0 <= v1_idx < node_count) and (0 <= v2_idx < node_count):
            distance = graph.get_distance(v1_idx, v2_idx)
            print(f"Distance between ({v1}, {v2}): {distance if distance is not None else 'Unreachable'}")

    # --- Case Study 6: Connected Components ---
    print("\n[Analysis 6: Connected Components]")
    count, components = graph.list_connected_components()
    print(f"Number of connected components: {count}")
    if components:
        print(f"Size of the largest component: {len(components[0])} vertices")
        print(f"Size of the smallest component: {len(components[-1])} vertices")

    # --- Case Study 7: Graph Diameter ---
    print("\n[Analysis 7: Graph Diameter]")
    diameter = graph.get_diameter()
    print(f"Diameter (approximate) of the graph: {diameter if diameter is not None else 'Infinite (disconnected graph)'}")

    # --- Output File Generation ---
    output_filename = f"graph_report_{os.path.basename(graph_file_path)}"
    graph.generate_graph_text_file(output_filename)
    print(f"\n[Extra] General graph report saved in: '{output_filename}'")
    
    print("=" * 60)


if __name__ == '__main__':
    # Place the names of the graph files you need to analyze here
    graph_files_to_analyze = ['your_graph_1.txt', 'your_graph_2.txt'] 
    
    for graph_file in graph_files_to_analyze:
        run_case_study(graph_file)