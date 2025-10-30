import time
import random
from typing import Type
from lib import GraphStructure
from lib.classes.dijkstra.dijkstra_heap import DijkstraHeap
from lib.classes.dijkstra.dijkstra_vector import DijkstraVector
from lib.classes.dijkstra.generic_dijkstra_structures_manager import GenericDijkstraStructuresManager

def case_1_min_distances(graph: GraphStructure, start_node: int) -> list[float]:
    # Run standard Dijkstra from start_node
    return graph.get_all_distances_and_fathers(start_node)

def case_2_dijkstra_performance_comparison(graph: GraphStructure) -> tuple[float, float]:
    
    # Inner function to time a specific Dijkstra implementation
    def measure_dijkstra_time(queue_type: Type[GenericDijkstraStructuresManager]) -> float:
        total_time = 0
        n = graph.get_node_count()
        # Sample 1 random node for the test
        for start_node in random.sample(range(1, n + 1), 1):
            start_time = time.perf_counter()
            graph.get_all_distances_and_fathers(start_node, queue_type)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        return total_time / 1
    
    # Measure Vector implementation time
    avg_time_vector = measure_dijkstra_time(DijkstraVector)
    # Measure Heap implementation time
    avg_time_heap = measure_dijkstra_time(DijkstraHeap)
    
    return avg_time_vector, avg_time_heap

def case_3_distance_between_researchers(graph: GraphStructure, researchers_names_file_path: str, start_researcher: str, end_researchers: list[str]) -> dict:
    """
    Executa o Dijkstra na rede de colaboração e retorna os dados brutos 
    necessários para a análise.
    """
    end_researchers_indexes = []
    researchers_names = [''] # Índice 0 é nulo
    start_researcher_index = None

    try:
        # Adicionado encoding='utf-8' para nomes com acentos (ex: Éva Tardos)
        with open(researchers_names_file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # Faz a leitura de forma mais segura, caso o nome tenha vírgula
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue
                
                i = int(parts[0])
                name = ','.join(parts[1:]).strip() # Pega o resto da linha
                
                # Garante que o array de nomes tenha o tamanho correto
                while len(researchers_names) <= i:
                    researchers_names.append('')
                
                researchers_names[i] = name
                
                if start_researcher == name:
                    start_researcher_index = i
                if name in end_researchers:
                    end_researchers_indexes.append(i)
                    
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de nomes de pesquisadores não encontrado em: {researchers_names_file_path}")
    except Exception as e:
        print(f"Erro ao ler o arquivo de pesquisadores: {e}")
        return {}

    if not start_researcher_index:
        raise ValueError(f'Pesquisador inicial "{start_researcher}" não foi encontrado no arquivo.')

    # Roda o Dijkstra
    distances_and_fathers = graph.get_all_distances_and_fathers(start_researcher_index)

    # Retorna todos os dados para o main.py processar
    return {
        "distances_and_fathers": distances_and_fathers,
        "researchers_names": researchers_names,
        "target_indices": end_researchers_indexes,
        "start_researcher_name": start_researcher
    }