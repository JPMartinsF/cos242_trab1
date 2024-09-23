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

graph = Graph()

test_graph_path = os.path.join("data", "test_graph.txt")
test_info_path = os.path.join("data", "test_graph_info.txt")

graph = test_read(test_graph_path, graph, representation="Adjacency Matrix")
test_info_file(graph, test_info_path)

graph = test_read(test_graph_path, graph, representation="Adjacency List")
bfs_list_result = test_bfs_adjacency_list(graph, start_node=1)

graph = test_read(test_graph_path, graph, representation="Adjacency Matrix")
bfs_matrix_result = test_bfs_adjacency_matrix(graph, start_node=1)

print("\nFinal BFS Results:")
print(f"BFS Adjacency List Result: {bfs_list_result}")
print(f"BFS Adjacency Matrix Result: {bfs_matrix_result}")
