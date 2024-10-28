import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def test_read(filename: str, representation: str, weighted:bool) -> Graph:
    graph = Graph()
    graph.initialize_graph_from_txt(filename, representation=representation, weighted=weighted)
    return graph

def test_info_file(graph: Graph, filename: str) -> None:
    graph.write_info_file(filename)

def test_bfs_adjacency_list(graph: Graph, start_node: int) -> list:
    result = graph.bfs_adjacency_list(start_node)
    print(f"BFS Adjacency List from node {start_node}: {result}")
    return result

def test_bfs_adjacency_matrix(graph: Graph, start_node: int) -> list:
    result = graph.bfs_adjacency_matrix(start_node)
    print(f"BFS Adjacency Matrix from node {start_node}: {result}")
    return result

def test_bfs_distance(graph: Graph, start_node: int, target_node: int) -> int:
    distance = graph.bfs_shortest_path(start_node, target_node)
    print(f"Distance between node {start_node} and node {target_node}: {distance}")
    return distance

def test_diameter(graph: Graph) -> int:
    diameter = graph.calculate_diameter()
    print(f"Graph Diameter: {diameter}")
    return diameter

def test_approximate_diameter(graph: Graph, sample_size: int) -> int:
    approximate_diameter = graph.calculate_approximate_diameter(sample_size)
    print(f"Approximate Diameter (sample size {sample_size}): {approximate_diameter}")
    return approximate_diameter

def test_connected_components(graph: Graph) -> dict:
    components = graph.find_connected_components()
    print(f"Connected Components: {components}")
    return components

def test_dfs_adjacency_list(graph: Graph, start_node: int) -> list:
    """Test DFS using adjacency list."""
    result = graph.dfs_adjacency_list(start_node)
    print(f"DFS Adjacency List from node {start_node}: {result}")
    return result

def test_dfs_adjacency_matrix(graph: Graph, start_node: int) -> list:
    """Test DFS using adjacency matrix."""
    result = graph.dfs_adjacency_matrix(start_node)
    print(f"DFS Adjacency Matrix from node {start_node}: {result}")
    return result

if __name__ == "__main__":
    test_graph_path = os.path.join("data", "part_2", "test_graph.txt")
    test_info_path = os.path.join("data", "part_2", "test_graph_info.txt")

    # print("\n--- Adjacency Matrix ---")
    # graph_matrix = test_read(test_graph_path, representation="Adjacency Matrix", weighted=True)
    # test_info_file(graph_matrix, test_info_path)
    # test_bfs_adjacency_matrix(graph_matrix, start_node=1)
    # test_dfs_adjacency_matrix(graph_matrix, start_node=1)
    print("\n--- Adjacency List ---")
    graph_list = test_read(test_graph_path, representation="Adjacency List", weighted=True)
    # test_info_file(graph_list, test_info_path)
    # test_bfs_adjacency_list(graph_list, start_node=1)
    # test_dfs_adjacency_list(graph_list, start_node=1)
    # test_bfs_distance(graph_list, start_node=1, target_node=5)
    # test_bfs_distance(graph_list, start_node=1, target_node=2)
    # test_bfs_distance(graph_list, start_node=1, target_node=3)
    # test_diameter(graph_list)
    # test_connected_components(graph_list)
    # sample_size = 3
    # test_approximate_diameter(graph_list, sample_size)

    print(graph_list.adjacency_list)
    print(graph_list.dijkstra(3))
    print(graph_list.dijkstra(3, True))


    # graph_file_number = "5"

    # graph_path = os.path.join("data", f"grafo_{graph_file_number}.txt")
    # info_path = os.path.join("data", f"grafo_{graph_file_number}_info.txt")

    # graph = test_read(graph_path, representation="Adjacency List")
    # test_info_file(graph, info_path)

    # print(graph.calculate_approximate_diameter(3))

    # print(list(aux.keys()))
    # print("LEN", len(aux))
    # print(max(aux), min(aux))



    # graph = test_read(graph_path, representation="Adjacency Matrix")
    # test_info_file(graph, info_path)

    # start_time = time.time()

    # print("loop")

    # # for i in range(100):
    # #     print(i)
    # graph.dfs(random.randint(1, graph.graph_size))
    #     # if (i+1) % 10 == 0:

    # elapsed_time = (time.time() - start_time)
    # print("Time spent MATRIX:", elapsed_time , "seconds")
    
    # # print("Memory used by MATRIX graph:", sys.getsizeof(graph.adjacency_matrix)/1000000, "mega bytes")
    # del graph


    

    # start_time = time.time()

    # print("AAAAA")
    # for i in range(1):
    #     print(i)
    #     graph.dfs(random.randint(1, graph.graph_size))
    
    # # print("Memory used by LIST graph:", sys.getsizeof(graph.adjacency_list)/1000000, "mega bytes")

    # elapsed_time = (time.time() - start_time)
    # print("Time spent LIST:", elapsed_time , "seconds")
    # pass

'''
test_graph
#1_0.1_#2
 |    /
 1  0.2
 | /
#5
 |  \
 2.3  5
 |     \
#4_-9.5_#3
'''
