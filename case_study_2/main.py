from lib import AdjacencyVector
from case_study_2.cases import case_1_min_distances, case_2_dijkstra_performance_comparison, case_3_distance_between_researchers

def get_path(distances_and_fathers: list[tuple[float, int | None]], end_node: int) -> list[int]:
    # Reconstructs the minimum path by backtracking from the end node
    path = []
    current_node = end_node

    if not distances_and_fathers or end_node >= len(distances_and_fathers) or distances_and_fathers[end_node][0] == float('inf'):
        return []

    while current_node is not None:
        path.append(current_node)
        father_index = distances_and_fathers[current_node][1]
        # Safety check for invalid father index
        if father_index is not None and father_index >= len(distances_and_fathers):
            print(f"ERROR: Invalid father index ({father_index}) while reconstructing path to {end_node}.")
            return []
        current_node = father_index

        # Safety check for cycles
        if current_node in path:
             print(f"ERROR: Cycle detected while reconstructing path to {end_node}.")
             return []

    return path[::-1] # Reverse to get start -> end order

def run_case_study_2_part_1(graph_file_path: str):
    # Executes case studies 1 and 2 for a given graph file

    print("=" * 60)
    print(f"Starting Case Study 1 and 2 on graph: {graph_file_path}")
    print("=" * 60)

    try:
        # Prefer Adjacency Vector for Dijkstra on potentially sparse graphs
        print("\nBuilding Adjacency Vector Representation...")
        graph = AdjacencyVector(graph_file_path)
    except FileNotFoundError:
        print(f"ERROR: Graph file '{graph_file_path}' not found.")
        return
    except Exception as e:
        print(f"ERROR loading graph {graph_file_path}: {e}")
        return

    # Case 1: Minimum Distances
    print("\n--- Case Study 1: Minimum Distances (Vertex 10) ---")
    start_node_case1 = 10
    target_nodes_case1 = [20, 30, 40, 50, 60]

    try:
        # Use case function to run Dijkstra (defaults to Heap implementation)
        all_distances = case_1_min_distances(graph, start_node=start_node_case1)

        print(f"Results starting from vertex {start_node_case1}:")
        for target_node in target_nodes_case1:
            if target_node >= len(all_distances):
                 print(f"\n  ERROR: Target node {target_node} is out of bounds for graph {graph_file_path}.")
                 continue

            distance, father = all_distances[target_node]
            print(f"\n  To vertex {target_node}:")
            if distance == float('inf'):
                print(f"    Distance: \u221E (Unreachable)")
                print(f"    Path: N/A")
            else:
                path = get_path(all_distances, target_node)
                path_str = ' -> '.join(map(str, path))
                print(f"    Distance: {distance:.2f} (via node {father})")
                print(f"    Path: {path_str}")

    except ValueError as ve: # Handles negative weights if raised by Dijkstra
         print(f"  WARNING: Could not calculate distances: {ve}")
    except Exception as e:
        print(f"  Unexpected ERROR calculating distances: {e}")


    # Case 2: Performance Comparison
    print("\n--- Case Study 2: Performance Comparison (Vector vs Heap) ---")
    try:
        avg_time_vector, avg_time_heap = case_2_dijkstra_performance_comparison(graph)
        print(f"Average time using Dijkstra with Vector: {avg_time_vector:.6f} seconds")
        print(f"Average time using Dijkstra with Heap:  {avg_time_heap:.6f} seconds")
    except ValueError as ve: # Handles negative weights
         print(f"  WARNING: Could not compare performance: {ve}")
    except Exception as e:
        print(f"  Unexpected ERROR comparing performance: {e}")
    print("-" * 60)

def run_case_study_2_part_2():
    # Executes case study 3 (collaboration network)

    print("\n" + "=" * 60)
    print("Starting Case Study 3: Collaboration Network")
    print("=" * 60)

    graph_path = 'case_study_2/graphs/rede_colaboracao.txt'
    names_path = 'case_study_2/graphs/rede_colaboracao_vertices.txt'

    try:
        print(f"Loading graph from: {graph_path}")
        graph = AdjacencyVector(graph_path)
    except FileNotFoundError:
        print(f"ERROR: File '{graph_path}' not found.")
        return
    except Exception as e:
        print(f"ERROR loading the collaboration network graph: {e}")
        return

    start_researcher = 'Edsger W. Dijkstra'
    end_researchers = [
        'Alan M. Turing',
        'J. B. Kruskal',
        'Jon M. Kleinberg',
        'Éva Tardos', # Ensure file encoding handles special characters
        'Daniel R. Figueiredo'
    ]

    try:
        print(f"Loading names from: {names_path}")
        result_data = case_3_distance_between_researchers(
            graph,
            names_path,
            start_researcher,
            end_researchers
        )

        if not result_data:
            print("Could not process the collaboration network case.")
            return

        distances_and_fathers = result_data["distances_and_fathers"]
        researchers_names = result_data["researchers_names"]
        target_indices = result_data["target_indices"]
        start_name = result_data["start_researcher_name"]

        print(f"\nCalculating minimum paths starting from: {start_name}\n")

        for target_index in target_indices:
            if not isinstance(target_index, int) or target_index >= len(researchers_names):
                print(f"ERROR: Invalid target index ({target_index}) found.")
                continue

            target_name = researchers_names[target_index]

            if target_index >= len(distances_and_fathers):
                 print(f"ERROR: Target index ({target_index}) out of range for Dijkstra results.")
                 continue

            distance, _ = distances_and_fathers[target_index]
            separator = "-" * (len(target_name) + 10)
            print(f"--- To {target_name} ---")

            if distance == float('inf'):
                print(f"  Distance: \u221E (Unreachable)")
                print(f"  Path: N/A")
            else:
                path_indices = get_path(distances_and_fathers, target_index)
                # Map indices back to names
                path_names = [researchers_names[i]
                              for i in path_indices
                              if i is not None and isinstance(i, int) and i < len(researchers_names)]

                print(f"  Distance: {distance:.2f}")
                print(f"  Path: {' -> '.join(path_names)}")
            print(f"{separator}\n")

    except FileNotFoundError as fnf:
        print(f"ERROR: File not found - {fnf}")
    except ValueError as ve:
         print(f"ERROR: Problem with data (e.g., researcher not found) - {ve}")
    except Exception as e:
        print(f"\n--- An unexpected error occurred while executing Case Study 3 ---")
        print(f"  Error Type: {type(e).__name__}")
        print(f"  Detail: {e}")
        print("  Please check the researcher names and file paths.")

if __name__ == '__main__':

    graph_files_to_analyze = [
        'case_study_2/graphs/grafo_W_1.txt',
        'case_study_2/graphs/grafo_W_2.txt',
        'case_study_2/graphs/grafo_W_3.txt',
        'case_study_2/graphs/grafo_W_4.txt',
        'case_study_2/graphs/grafo_W_5.txt'
    ]

    print("Starting execution of AP2 Case Studies...")

    for graph_file in graph_files_to_analyze:
        run_case_study_2_part_1(graph_file)

    run_case_study_2_part_2()

    print("\n" + "=" * 60)
    print("AP2 Case Studies completed.")
    print("=" * 60)