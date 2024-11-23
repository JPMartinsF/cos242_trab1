from collections import deque
from core import AdjacencyList, AdjacencyMatrix

class GraphAlgorithms:
    """Implements traversal algorithms for the graph."""

    def __init__(self, representation):
        self.representation = representation

    def bfs(self, start_node: int):
        """Chooses the appropriate BFS method based on the representation type.

        Args:
            start_node (int): The node from which to start BFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
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

    def dfs(self, start_node: int):
        """
        Performs DFS based on the graph representation (Adjacency List or Matrix).

        Args:
            start_node (int): The node from which to start DFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        if isinstance(self.representation, AdjacencyList):
            adj_list = self.representation.get_representation()
            visited = set()
            parents = {start_node: None}
            dfs_order = []
            stack = [start_node]

            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    dfs_order.append(node)
                    for neighbor in adj_list[node]:
                        if neighbor not in visited:
                            stack.append(neighbor)
                            parents[neighbor] = node
            return dfs_order, parents

        elif isinstance(self.representation, AdjacencyMatrix):
            matrix = self.representation.get_representation()
            visited = set()
            dfs_order = []
            stack = [start_node - 1]

            def _dfs(node):
                visited.add(node)
                dfs_order.append(node + 1)
                for neighbor, weight in enumerate(matrix[node]):
                    if neighbor not in visited and weight != float('inf') and weight != 0:
                        _dfs(neighbor)

            _dfs(start_node - 1)
            return dfs_order
        else:
            raise ValueError("Unsupported graph representation.")