import heapq
from collections import deque
from core.graph_representations import AdjacencyList, AdjacencyMatrix
from collections import defaultdict

class GraphTraversal:
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
        

class GraphAlgorithms:
    """Implements algorithms like Dijkstra."""

    def __init__(self, representation):
        self.representation = representation

    def dijkstra(self, start_node: int):
        """Implements Dijkstra's algorithm for shortest paths."""
        if isinstance(self.representation, AdjacencyList):
            adj_list = self.representation.get_representation()

            dist = {node: float("inf") for node in adj_list}
            dist[start_node] = 0
            priority_queue = [(0, start_node)]
            parents = {node: None for node in adj_list}

            while priority_queue:
                current_dist, current_node = heapq.heappop(priority_queue)

                for neighbor, weight in adj_list[current_node].items():
                    new_dist = current_dist + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        parents[neighbor] = current_node
                        heapq.heappush(priority_queue, (new_dist, neighbor))

            return dist, parents

        elif isinstance(self.representation, AdjacencyMatrix):
            raise NotImplementedError("Dijkstra's algorithm for Adjacency Matrix is not implemented yet.")
        else:
            raise ValueError("Unsupported graph representation.")
        
class GraphFlowNetwork:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.residual = defaultdict(dict)

    def add_edge(self, u, v, capacity):
        """Adds an edge with capacity to the graph."""
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self.graph[u][v] = {"capacity": capacity, "flow": 0}
        self.graph[v][u] = {"capacity": 0, "flow": 0}  # Reverse edge for residual graph

    def build_residual_graph(self):
        """Builds the residual graph."""
        self.residual.clear()
        for u in self.graph:
            for v, data in self.graph[u].items():
                capacity = data["capacity"] - data["flow"]
                if capacity > 0:
                    self.residual[u][v] = {"capacity": capacity, "original": 1}
                if data["flow"] > 0:
                    self.residual[v][u] = {"capacity": data["flow"], "original": 0}

    def find_augmenting_path(self, source, bottleneck):
        """Finds an augmenting path using BFS and returns the path and bottleneck."""
        parent = {source: None}
        queue = deque([source])
        while queue:
            current = queue.popleft()
            if current == bottleneck:
                break
            for neighbor, data in self.residual[current].items():
                if neighbor not in parent and data["capacity"] > 0:
                    parent[neighbor] = current
                    queue.append(neighbor)

        if bottleneck not in parent:
            return None, 0

        path = []
        current = bottleneck
        bottleneck = float("inf")
        while parent[current] is not None:
            prev = parent[current]
            path.append((prev, current))
            bottleneck = min(bottleneck, self.residual[prev][current]["capacity"])
            current = prev
        path.reverse()
        return path, bottleneck

    def update_flows(self, path, bottleneck):
        """Updates flows in the graph and residual graph."""
        for u, v in path:
            self.graph[u][v]["flow"] += bottleneck
            self.graph[v][u]["flow"] -= bottleneck

    def ford_fulkerson(self, source, target, bottleneck, save_to_file=None):
        """Executes the Ford-Fulkerson algorithm to find the maximum flow."""
        max_flow = 0
        while True:
            self.build_residual_graph()
            path, bottleneck = self.find_augmenting_path(source, target)
            if not path or bottleneck == 0:
                break
            self.update_flows(path, bottleneck)
            max_flow += bottleneck

        if save_to_file:
            self.save_flows_to_file(save_to_file)

        return max_flow

    def save_flows_to_file(self, filename):
        """Saves the flow information to a file."""
        with open(filename, "w") as file:
            for u in self.graph:
                for v, data in self.graph[u].items():
                    if data["flow"] > 0:
                        file.write(f"{u} {v} {data['flow']}\n")
