from lib import AdjacencyVector
import random
import time

def run_case_study_3(graph_file_path: str) -> None:
    print("=" * 60)
    print(f"Case Study 3: Analyzing graph from file '{graph_file_path}'")
    print("=" * 60)

    graph = AdjacencyVector(graph_file_path, is_directed=True)

    try:
        bellman_ford_distances = graph.get_all_distances_and_sons_to_end_node(100)
        print(f"Distances to node 100:")
        print(
            f"From node 10: {bellman_ford_distances[10][0]}"
            f", From node 20: {bellman_ford_distances[20][0]}"
            f", From node 30: {bellman_ford_distances[30][0]}"
        )
    except ValueError as err:
        print(err)

    print("\nCalculating average execution time for Bellman-Ford algorithm...")
    total_time = 0
    runs = 5
    n = graph.get_node_count()
    random_nodes = random.sample(range(1, n + 1), runs)
    for node in random_nodes:
        start_time = time.perf_counter()
        print(f'started run for node {node}')
        try:
            graph.get_all_distances_and_sons_to_end_node(node)
            print(f'run for node {node} ended')
        except ValueError as err:
            print(err)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    avg_bellman_ford_time = total_time / runs
    print(f"Average execution time (Bellman-Ford): {avg_bellman_ford_time:.2f} seconds")

    if graph.has_negative_weight:
        print("Graph contains negative weight edges; Dijkstra's algorithm may not be applicable.")
        return

    print("\nRunning Dijkstra's algorithm on the reversed graph...")
    reversed_graph = AdjacencyVector(graph_file_path, is_directed=True, reverse=True)
    dijkstra_distances = reversed_graph.get_all_distances_and_fathers_from_start_node(100)
    print(f"Distances to node 100:")
    print(
        f"From node 10: {dijkstra_distances[10][0]}"
        f", From node 20: {dijkstra_distances[20][0]}"
        f", From node 30: {dijkstra_distances[30][0]}"
    )

    print("\nCalculating average execution time for Dijkstra's algorithm...")
    total_time = 0
    for node in random_nodes:
        start_time = time.perf_counter()
        reversed_graph.get_all_distances_and_fathers_from_start_node(node)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    avg_dijkstra_time = total_time / runs
    print(f"Average execution time (Dijkstra): {avg_dijkstra_time:.2f} seconds")


if __name__ == '__main__':
    graph_files_to_analyze = [
        'case_study_3/graphs/grafo_W_2.txt',
    ]
    for graph_file in graph_files_to_analyze:
        run_case_study_3(graph_file)

    print("=" * 60)
    print("Case Study 3 Completed Successfully.")
    print("=" * 60)