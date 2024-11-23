import statistics

from core.graph_representations import AdjacencyList
from core.graph_representations import AdjacencyMatrix

class GraphMetrics:
    """Calculates metrics for a graph."""

    def __init__(self, representation):
        self.representation = representation

    def calculate_degree_metrics(self):
        """Calculates degree metrics like min, max, mean, and median."""

        degrees = []
        if isinstance(self.representation, AdjacencyMatrix):
            matrix = self.representation.get_representation()
            degrees = [sum(1 for weight in row if weight != float('inf') and weight != 0) for row in matrix]
        elif isinstance(self.representation, AdjacencyList):
            adj_list = self.representation.get_representation()
            degrees = [len(neighbors) if isinstance(neighbors, list) else len(neighbors.keys()) for neighbors in adj_list.values()]

        return {
            "min_degree": min(degrees),
            "max_degree": max(degrees),
            "mean_degree": sum(degrees) / len(degrees),
            "median_degree": statistics.median(degrees),
        }
