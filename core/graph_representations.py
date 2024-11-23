class AdjacencyMatrix:
    """Manages the adjacency matrix representation of a graph."""

    def __init__(self, size: int):
        self.size = size
        self.matrix = self._initialize_matrix()

    def _initialize_matrix(self):
        """Initializes an adjacency matrix with infinite weights."""
        import numpy as np
        matrix = np.full((self.size, self.size), float('inf'))
        np.fill_diagonal(matrix, 0)
        return matrix

    def add_edge(self, u_node: int, v_node: int, weight: float = 1):
        """Adds an edge to the adjacency matrix."""
        self.matrix[u_node - 1][v_node - 1] = weight
        if weight == 1:  # Assuming undirected graph if weight = 1
            self.matrix[v_node - 1][u_node - 1] = weight

    def get_representation(self):
        return self.matrix


class AdjacencyList:
    """Manages the adjacency list representation of a graph."""

    def __init__(self, size: int, weighted: bool):
        self.size = size
        self.weighted = weighted
        self.list = self._initialize_list()

    def _initialize_list(self):
        """Initializes an adjacency list."""
        if self.weighted:
            return {i: {} for i in range(1, self.size + 1)}
        else:
            return {i: [] for i in range(1, self.size + 1)}

    def add_edge(self, u_node: int, v_node: int, weight: float = 1):
        """Adds an edge to the adjacency list."""
        if self.weighted:
            self.list[u_node][v_node] = weight
            self.list[v_node][u_node] = weight
        else:
            self.list[u_node].append(v_node)
            self.list[v_node].append(u_node)

    def get_representation(self):
        return self.list
