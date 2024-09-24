import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def test_read(filename: str, graph: Graph, representation: str = "Adjacency Matrix") -> Graph:
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

graph = Graph()

test_graph_path = os.path.join("data", "test_graph.txt")
test_info_path = os.path.join("data", "test_graph_info.txt")

graph = test_read(test_graph_path, graph, representation="Adjacency Matrix")

test_info_file(graph, test_info_path)
bfs_list_result = test_bfs_adjacency_list(graph, start_node=1)
bfs_matrix_result = test_bfs_adjacency_matrix(graph, start_node=1)
distance_result = test_bfs_distance(graph, start_node=1, target_node=4)

print(f"BFS Adjacency List Result: {bfs_list_result}")
print(f"BFS Adjacency Matrix Result: {bfs_matrix_result}")
print(f"Distance Result: {distance_result}")