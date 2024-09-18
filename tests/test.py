import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def test_read(filename: str, graph: Graph) -> Graph:
    # Initialize the graph from the file
    graph.initialize_graph_from_txt(filename)
    return graph

graph = Graph()
graph = test_read(r"data\grafo_1.txt", graph)
True
