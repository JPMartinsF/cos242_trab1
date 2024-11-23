import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Graph

def test_read(filename: str, representation: str, weighted: bool) -> Graph:
    """Initializes a graph from a text file."""
    size = 0
    with open(filename, "r", encoding="utf-8") as file:
        size = int(file.readline().strip())  # First line specifies the graph size

    graph = Graph(size=size, representation=representation, weighted=weighted)

    with open(filename, "r", encoding="utf-8") as file:
        next(file)  # Skip the first line
        for line in file:
            edge_data = line.split()
            if weighted and len(edge_data) == 3:
                u, v, weight = int(edge_data[0]), int(edge_data[1]), float(edge_data[2])
                graph.add_edge(u, v, weight)
            elif len(edge_data) == 2:
                u, v = int(edge_data[0]), int(edge_data[1])
                graph.add_edge(u, v)

    return graph

def test_info_file(graph: Graph, filename: str) -> None:
    """Delegates saving graph info to the GraphIO class."""
    graph.file_io.save_graph_to_file(filename, graph)

def test_bfs(graph: Graph, start_node: int) -> list:
    """Tests BFS traversal."""
    result = graph.bfs(start_node)
    print(f"BFS from node {start_node}: {result}")
    return result

def test_dfs(graph: Graph, start_node: int) -> list:
    """Tests DFS traversal."""
    result = graph.dfs(start_node)
    print(f"DFS from node {start_node}: {result}")
    return result

def test_dijkstra(graph: Graph, start_node: int) -> tuple:
    """Tests Dijkstra's algorithm."""
    distances, parents = graph.dijkstra(start_node)
    print(f"Dijkstra's algorithm from node {start_node}:")
    print(f"Distances: {distances}")
    print(f"Parents: {parents}")
    return distances, parents

if __name__ == "__main__":
    test_graph_path = os.path.join("data", "part_2", "test_graph.txt")
    test_info_path = os.path.join("data", "part_2", "test_graph_info.txt")

    print("\n--- Adjacency List ---")
    graph_list = test_read(test_graph_path, representation="Adjacency List", weighted=True)

    # Test graph metrics and info writing
    test_info_file(graph_list, test_info_path)

    # Test BFS and DFS
    test_bfs(graph_list, start_node=1)
    test_dfs(graph_list, start_node=1)

    # Test Dijkstra's algorithm
    test_dijkstra(graph_list, start_node=1)
