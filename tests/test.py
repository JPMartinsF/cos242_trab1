import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def test_read(filename: str, representation: str) -> Graph:
    graph = Graph()
    graph.initialize_graph_from_txt(filename, representation=representation)
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

def test_connected_components(graph: Graph) -> dict:
    components = graph.find_connected_components()
    print(f"Connected Components: {components}")
    return components

if __name__ == "__main__":
    test_graph_path = os.path.join("data", "test_graph.txt")
    test_info_path = os.path.join("data", "test_graph_info.txt")

    print("\n--- Adjacency Matrix ---")
    graph_matrix = test_read(test_graph_path, representation="Adjacency Matrix")
    test_info_file(graph_matrix, test_info_path)
    test_bfs_adjacency_matrix(graph_matrix, start_node=1)

    print("\n--- Adjacency List ---")
    graph_list = test_read(test_graph_path, representation="Adjacency List")
    test_info_file(graph_list, test_info_path)
    test_bfs_adjacency_list(graph_list, start_node=1)
    test_bfs_distance(graph_list, start_node=1, target_node=5)
    test_bfs_distance(graph_list, start_node=1, target_node=2)
    test_bfs_distance(graph_list, start_node=1, target_node=3)
    test_diameter(graph_list)
    test_connected_components(graph_list)

'''
test_graph
1_2
|/
5
|\
4 3
'''