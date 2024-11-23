from core.graph_representations import AdjacencyList, AdjacencyMatrix
from core.graph_algorithms import GraphAlgorithms, GraphTraversal
from core.graph_metrics import GraphMetrics
from core.graph_io import GraphIO

class Graph:
    """High-level class managing the graph by delegating tasks to appropriate classes."""

    def __init__(self, size: int, representation: str, weighted: bool = False, directed: bool = False):
        self.size = size
        self.weighted = weighted
        self.is_directed = directed
        self.representation = (
            AdjacencyMatrix(size) if representation == "Adjacency Matrix" else AdjacencyList(size, weighted)
        )
        self.metrics = GraphMetrics(self.representation)
        self.traversal = GraphTraversal(self.representation)
        self.algorithms = GraphAlgorithms(self.representation)
        self.file_io = GraphIO

    def add_edge(self, u: int, v: int, weight: float = 1):
        """Adds an edge to the graph."""
        self.representation.add_edge(u, v, weight)

    def get_degree_metrics(self):
        """Fetches degree metrics."""
        return self.metrics.calculate_degree_metrics()

    def bfs(self, start_node: int):
        """Delegates BFS to the traversal class."""
        return self.traversal.bfs(start_node)

    def dfs(self, start_node: int):
        """Delegates DFS to the traversal class."""
        return self.traversal.dfs(start_node)

    def dijkstra(self, start_node: int):
        """Delegates Dijkstra's algorithm to the algorithms class."""
        return self.algorithms.dijkstra(start_node)
