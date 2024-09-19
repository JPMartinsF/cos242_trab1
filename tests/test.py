import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def test_read(filename: str, graph: Graph) -> Graph:
    # Initialize the graph from the file
    graph.initialize_graph_from_txt(filename, representation="Adjacency Matrix")
    return graph

def test_info_file(graph: Graph, filename: str) -> None:
    graph.write_info_file(filename)
    return

graph = Graph()
graph = test_read(r"data\test_graph.txt", graph)
test_info_file(graph, r"data\test_graph_info.txt")

True