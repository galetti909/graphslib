import random
import os

from lib import AdjacencyMatrix, AdjacencyVector

from case_study_1.cases import (
    case_1_memory_analysis,
    cases_2_3_bfs_dfs_performance,
    case_4_parents_in_search_trees,
    case_5_distance_between_vertices,
    case_6_connected_components,
    case_7_graph_diameter
)

def show_results(case_1, case_2, case_3, case_4, case_5, case_6, case_7) -> None:
    print("\n--- Case Study Results ---\n")
    
    print("Case 1: Memory Usage (in bytes)")
    if case_1[0] is None:
        print("  Adjacency Matrix: Analysis skipped due to memory error")
    else:
        print(f"  Adjacency Matrix: {case_1[0]:,} mega bytes")
    print(f"  Adjacency Vector: {case_1[1]:,} mega bytes\n")

    print("Case 2 & 3: Average Search Times (in seconds)")
    if case_2[0] is None:
        print("  Adjacency Matrix: Analysis skipped due to memory error")
    else:
        print(f"  Adjacency Matrix - BFS: {case_2[0]:.6f} s, DFS: {case_2[1]:.6f} s")
    print(f"  Adjacency Vector - BFS: {case_3[0]:.6f} s, DFS: {case_3[1]:.6f} s\n")

    print("Case 4: Parents in Search Trees")
    for i, parents in enumerate(case_4, start=1):
        print(f"  Start Node {i}: Parents -> {parents}\n")

    print("Case 5: Distances Between Vertex Pairs")
    for i, distance in enumerate(case_5, start=1):
        node_pair = [(10, 20), (10, 30), (20, 30)][i-1]
        dist_str = distance if distance is not None else 'Unreachable'
        print(f"  Distance between nodes {node_pair}: {dist_str}\n")

    print("Case 6: Connected Components")
    num_components, size_greatest_component = case_6
    print(f"  Number of Connected Components: {num_components}")
    print(f"  Size of Greatest Component: {size_greatest_component}\n")

    print("Case 7: Graph Diameter")
    diameter = case_7
    diameter_str = diameter if diameter is not None else 'Undefined (Disconnected Graph)'
    print(f"  Graph Diameter: {diameter_str}\n")

def run_case_study(graph_file_path: str) -> list[tuple[float, float, float]] | None:
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

    # --- Part 1: Data Analysis (case 1, 2, 3) ---
    case_1 = []

    # Adjacency Matrix
    print("\nBuilding Adjacency Matrix Representation...")
    try:
        graph = AdjacencyMatrix(graph_file_path)
        case_1.append(case_1_memory_analysis(graph))
        node_count = graph.get_node_count()
        num_runs = min(100, node_count)
        start_nodes = random.sample(range(1, node_count + 1), num_runs)
        print("Measuring BFS and DFS performance...")
        bfs_avg_time, dfs_avg_time = cases_2_3_bfs_dfs_performance(graph, start_nodes)
        case_2 = (bfs_avg_time, dfs_avg_time)
    except MemoryError as e:
        print(f"Skipping Adjacency Matrix analysis due to memory error: {e}")
        case_1.append(None)
        case_2 = (None, None)

    # Adjacency Vector
    print("\nBuilding Adjacency Vector Representation...")
    graph = AdjacencyVector(graph_file_path)
    case_1.append(case_1_memory_analysis(graph))
    node_count = graph.get_node_count()
    num_runs = min(100, node_count)
    start_nodes = random.sample(range(1, node_count + 1), num_runs)
    print("Measuring BFS and DFS performance...")
    bfs_avg_time, dfs_avg_time = cases_2_3_bfs_dfs_performance(graph, start_nodes)
    case_3 = (bfs_avg_time, dfs_avg_time)

    # --- Part 2: Direct Answers ---
    print("Searching for direct answers to cases 4-7...")
    case_4 = []
    start_nodes = [1, 2, 3]
    target_nodes = [10, 20, 30]
    for start_node in start_nodes:
        case_4.append(case_4_parents_in_search_trees(graph, start_node, target_nodes))

    print("5")
    case_5 = []
    pairs = [(10, 20), (10, 30), (20, 30)]
    for node_1, node_2 in pairs:
        distance = case_5_distance_between_vertices(graph, node_1, node_2)
        case_5.append(distance)

    print("6")
    case_6 = case_6_connected_components(graph)

    print("7")
    case_7 = case_7_graph_diameter(graph)

    print("=" * 60)
    print("\nCase Study Completed Successfully.")
    print("=" * 60)

    show_results(case_1, case_2, case_3, case_4, case_5, case_6, case_7)

if __name__ == '__main__':
    graph_files_to_analyze = [
        'case_study_1/graphs/grafo_1.txt', 
        'case_study_1/graphs/grafo_2.txt', 
        'case_study_1/graphs/grafo_3.txt', 
        'case_study_1/graphs/grafo_4.txt', 
        'case_study_1/graphs/grafo_5.txt', 
        'case_study_1/graphs/grafo_6.txt'
    ]
    for graph_file in graph_files_to_analyze:
        run_case_study(graph_file)