import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def test_read(filename: str, graph: Graph, representation: str = "Adjacency Matrix") -> Graph:
    graph.initialize_graph_from_txt(filename, representation=representation)
    return graph

def test_info_file(graph: Graph, filename: str) -> None:
    graph.write_info_file(filename)

def test_bfs_adjacency_list(graph: Graph, start_node: int, expected_output: list) -> None:
    result = graph.bfs_adjacency_list(start_node)
    assert result == expected_output, f"BFS Adjacency List failed. Expected: {expected_output}, Got: {result}"
    print(f"BFS Adjacency List passed for start node {start_node}.")

def test_bfs_adjacency_matrix(graph: Graph, start_node: int, expected_output: list) -> None:
    result = graph.bfs_adjacency_matrix(start_node)
    assert result == expected_output, f"BFS Adjacency Matrix failed. Expected: {expected_output}, Got: {result}"
    print(f"BFS Adjacency Matrix passed for start node {start_node}.")

graph = Graph()

test_graph_path = os.path.join("data", "test_graph.txt")
test_info_path = os.path.join("data", "test_graph_info.txt")

graph = test_read(test_graph_path, graph, representation="Adjacency Matrix")
test_info_file(graph, test_info_path)

expected_bfs_order = [1, 2, 3, 4, 5]

graph = test_read(test_graph_path, graph, representation="Adjacency List")
test_bfs_adjacency_list(graph, start_node=1, expected_output=expected_bfs_order)

graph = test_read(test_graph_path, graph, representation="Adjacency Matrix")
test_bfs_adjacency_matrix(graph, start_node=1, expected_output=expected_bfs_order)
