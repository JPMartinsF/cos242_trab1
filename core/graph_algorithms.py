from collections import deque
from core import AdjacencyList, AdjacencyMatrix

class GraphAlgorithms:
    """Implements traversal algorithms for the graph."""

    def __init__(self, representation):
        self.representation = representation

    def bfs(self, start_node: int):
        """Performs BFS."""

        if isinstance(self.representation, AdjacencyList):
            adj_list = self.representation.get_representation()
            visited = set()
            queue = deque([start_node])
            bfs_order = []

            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.add(node)
                    bfs_order.append(node)
                    queue.extend(adj_list[node] if isinstance(adj_list[node], list) else adj_list[node].keys())
            return bfs_order

        elif isinstance(self.representation, AdjacencyMatrix):
            matrix = self.representation.get_representation()
            visited = set()
            queue = deque([start_node - 1])
            bfs_order = []

            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.add(node)
                    bfs_order.append(node + 1)
                    neighbors = [i for i, weight in enumerate(matrix[node]) if weight != float('inf') and weight != 0]
                    queue.extend(neighbors)
            return bfs_order
        else:
            raise ValueError("Unsupported graph representation.")
