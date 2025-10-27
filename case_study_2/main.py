from lib import AdjacencyVector
from case_study_2.cases import case_1_min_distances, case_2_dijkstra_performance_comparison, case_3_distance_between_researchers

def get_path(distances_and_fathers: list[tuple[float, int | None]], end_node: int) -> list[int]:
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        _, current_node = distances_and_fathers[current_node]
    return path[::-1]

def run_case_study_2_part_1(graph_file_path: str):

    print("=" * 60)
    print(f"Starting Case Study 2 on graph: {graph_file_path}")
    print("=" * 60)

    # Build Adjacency Vector Representation
    print("\nBuilding Adjacency Vector Representation...")
    graph = AdjacencyVector(graph_file_path)

    # Case 1: Minimum Distances from Node 10
    print("Calculating minimum distances from node 10...")
    min_distances = case_1_min_distances(graph, start_node=10)
    print(f"Minimum distances from node 10:")
    print(f"10 to 20: {min_distances[20]}")
    print(' -> '.join(map(str, get_path(min_distances, 20))))
    print(f"10 to 30: {min_distances[30]}")
    print(' -> '.join(map(str, get_path(min_distances, 30))))
    print(f"10 to 40: {min_distances[40]}")
    print(' -> '.join(map(str, get_path(min_distances, 40))))
    print(f"10 to 50: {min_distances[50]}")
    print(' -> '.join(map(str, get_path(min_distances, 50))))
    print(f"10 to 60: {min_distances[60]}")
    print(' -> '.join(map(str, get_path(min_distances, 60))))



    # Case 2: Dijkstra Performance Comparison
    print("Comparing Dijkstra performance with different data structures...")
    avg_time_vector, avg_time_heap = case_2_dijkstra_performance_comparison(graph)
    print(f"Average time using Dijkstra with Vector: {avg_time_vector:.6f} seconds")
    print(f"Average time using Dijkstra with Heap: {avg_time_heap:.6f} seconds")
    return

def run_case_study_2_part_2():
    # Case 3: Distance Between Dijkstra and other researchers
    graph = AdjacencyVector('case_study_2/graphs/rede_colaboracao.txt')
    researchers_names_file_path = 'case_study_2/graphs/rede_colaboracao_vertices.txt'
    start_researcher = 'Edsger W. Dijkstra'
    end_researchers = ['Alan M. Turing', 'J. B. Kruskal', 'Jon M. Kleinberg', 'Éva Tardos', 'Daniel R. Figueiredo']
    print("Calculating distances between Dijkstra and other researchers...")
    result = case_3_distance_between_researchers(graph, researchers_names_file_path, start_researcher, end_researchers)
    for item in result:
        for name, (distance, father) in item.items():
            print(f"Distance from {start_researcher} to {name}: {distance} (via {father})")

if __name__ == '__main__':
    graph_files_to_analyze = [
        'case_study_2/graphs/grafo_W_1.txt',
    ]
    for graph_file in graph_files_to_analyze:
        run_case_study_2_part_1(graph_file)
    run_case_study_2_part_2()

    print("=" * 60)
    print("Case Study 2 Completed Successfully.")
    print("=" * 60)