import statistics
import numpy as np
import random
from heapq import heapify, heappop, heappush

class Graph:
    """
    Represents a graph that can be initialized from a source file
    and supports adjacency matrix and adjacency list representations.
    Also calculates node degrees, mean, median, and saves graph info to a file.
    """

    def __init__(self) -> None:
        """Initializes the graph with default attributes."""
        self.graph_size: int = 0
        self.graph_edges: list = []
        self.node_degrees: dict = {}
        self.mean_grade: float = 0.0
        self.median_grade: int = 0
        self.min_degree: int = None
        self.max_degree: int = None
        self.adjacency_matrix: list[list] = None
        self.adjacency_list: list[list] = None
        self.is_weighted: bool = False
        self.has_negative_weight: bool = False

    def initialize_graph_from_txt(self, file_name: str, representation: str, weighted: bool) -> None:
        """
        Initializes the graph from a text file.

        Args:
            file_name (str): The name of the file to read the graph from.
            representation (str): The representation wanted ('Adjacency Matrix' or 'Adjacency List').
        """
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                self.graph_size = int(file.readline().strip())
                self.graph_edges = []

                if representation == "Adjacency Matrix":
                    self.adjacency_matrix = self._initialize_adjacency_matrix()
                elif representation == "Adjacency List":
                    self.adjacency_list = self._initialize_adjacency_list(weighted=weighted)
                else:
                    raise ValueError(f"Unsupported representation: {representation}")

                for line in file.readlines():
                    edge_data = line.split()
                    if len(edge_data) == 2:
                        u_node, v_node = int(edge_data[0]), int(edge_data[1])
                        self.graph_edges.append((u_node, v_node))

                        self.node_degrees[u_node] = self.node_degrees.get(u_node, 0) + 1
                        self.node_degrees[v_node] = self.node_degrees.get(v_node, 0) + 1

                        if self.adjacency_matrix is not None:
                            self._add_edge_to_matrix(u_node, v_node)
                        elif self.adjacency_list is not None:
                            self._add_edge_to_list(u_node, v_node)
                    if len(edge_data) == 3:
                        self.is_weighted = True
                        u_node, v_node, edge_weigth = int(edge_data[0]), int(edge_data[1]), float(edge_data[2])
                        self.graph_edges.append((u_node, v_node))

                        if edge_weigth < 0:
                            self.has_negative_weight = True

                        self.node_degrees[u_node] = self.node_degrees.get(u_node, 0) + 1
                        self.node_degrees[v_node] = self.node_degrees.get(v_node, 0) + 1

                        if self.adjacency_matrix is not None:
                            self._add_weighted_edge_to_matrix(u_node, v_node, edge_weigth)
                        elif self.adjacency_list is not None:
                            self._add_weighted_edge_to_list(u_node, v_node, edge_weigth)
                    else:
                        print(f"Invalid node data: {line.strip()}")

                self._calculate_node_metrics()
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    def _initialize_adjacency_matrix(self):
        """Initializes an adjacency matrix for the graph."""
        matrix = np.full((self.graph_size, self.graph_size), np.inf)
        np.fill_diagonal(matrix, 0)
        return matrix

    def _initialize_adjacency_list(self, weighted):
        """Initializes an adjacency list for the graph."""
        return {i: {} if weighted else [] for i in range(1, self.graph_size + 1)}

    def _add_edge_to_matrix(self, u_node: int, v_node: int) -> None:
        """Adds a edge to the adjacency matrix."""
        self.adjacency_matrix[u_node - 1][v_node - 1] = 1
        self.adjacency_matrix[v_node - 1][u_node - 1] = 1

    def _add_edge_to_list(self, u_node: int, v_node: int) -> None:
        """Adds a edge to the adjacency list."""
        self.adjacency_list[u_node].append(v_node)
        self.adjacency_list[v_node].append(u_node)

    def _add_weighted_edge_to_matrix(self, u_node: int, v_node: int, edge_weigth: float) -> None:
        """Adds a weighted edge to the adjacency matrix."""
        self.adjacency_matrix[u_node - 1][v_node - 1] = edge_weigth
        self.adjacency_matrix[v_node - 1][u_node - 1] = edge_weigth

    def _add_weighted_edge_to_list(self, u_node: int, v_node: int, edge_weigth: float) -> None:
        """Adds a weighted edge to the adjacency list."""
        self.adjacency_list[u_node][v_node] = edge_weigth
        self.adjacency_list[v_node][u_node] = edge_weigth

    def _calculate_node_metrics(self) -> None:
        """Calculates the min, max, mean, and median degrees of the graph's nodes."""
        if self.node_degrees:
            degrees = list(self.node_degrees.values())
            self.min_degree = min(degrees)
            self.max_degree = max(degrees)
            self.mean_grade = sum(degrees) / len(degrees)
            self.median_grade = statistics.median(degrees)

    def write_info_file(self, filename: str) -> None:
        """Writes the graph's statistical information to a file.

        Args:
            filename (str): The file to save the graph information.
        """
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Graph Size: {self.graph_size}\n")
            file.write(f"Number of edges: {len(self.graph_edges)}\n")
            file.write(f"Min Degree: {self.min_degree}\n")
            file.write(f"Max Degree: {self.max_degree}\n")
            file.write(f"Mean Degree: {self.mean_grade}\n")
            file.write(f"Median Degree: {self.median_grade}\n")

    def bfs(self, start_node: int) -> list:
        """Chooses the appropriate BFS method based on the representation type.

        Args:
            start_node (int): The node from which to start BFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        if self.adjacency_list is not None:
            return self.bfs_adjacency_list(start_node)
        elif self.adjacency_matrix is not None:
            return self.bfs_adjacency_matrix(start_node)
        else:
            raise ValueError("Graph representation is not initialized.")

    def bfs_adjacency_list(self, start_node: int) -> list:
        """Performs BFS on the adjacency list representation of the graph.

        Args:
            start_node (int): The starting node for BFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        if start_node not in self.adjacency_list:
            print(f"Start node {start_node} is not in the graph.")
            return []

        visited = set()
        parents = {start_node: None}
        bfs_order = []
        queue = [start_node]

        visited.add(start_node)

        while queue:
            current_node = queue[0]
            queue = queue[1:]
            bfs_order.append(current_node)

            for neighbor in self.adjacency_list[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = current_node

        return (bfs_order, parents)

    def bfs_adjacency_matrix(self, start_node: int) -> list:
        """Performs BFS on the adjacency matrix representation of the graph.

        Args:
            start_node (int): The starting node for BFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        if start_node < 1 or start_node > self.graph_size:
            print(f"Start node {start_node} is not in the valid node range.")
            return []

        visited = set()
        bfs_order = []
        queue = [start_node - 1]

        visited.add(start_node - 1)

        while queue:
            current_node = queue[0]
            queue = queue[1:]
            bfs_order.append(current_node + 1)

            for neighbor in range(self.graph_size):
                if neighbor not in visited:
                    if self.adjacency_matrix[current_node][neighbor] == 1:
                        visited.add(neighbor)
                        queue.append(neighbor)

        return bfs_order

    def dfs(self, start_node: int) -> list:
        """
        Performs DFS based on the graph representation (Adjacency List or Matrix).

        Args:
            start_node (int): The node from which to start DFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        if self.adjacency_list is not None:
            return self.dfs_adjacency_list(start_node)
        elif self.adjacency_matrix is not None:
            return self.dfs_adjacency_matrix(start_node)
        else:
            raise ValueError("Graph representation is not initialized.")

    def dfs_adjacency_list(self, start_node: int) -> list:
        """
        Performs an iterative DFS on the adjacency list representation of the graph.

        Args:
            start_node (int): The starting node for DFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        visited = set()
        parents = {start_node: None}
        dfs_order = []
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                dfs_order.append(node)
                for neighbor in self.adjacency_list[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        parents[neighbor] = node

        return (dfs_order, parents)

    def dfs_adjacency_matrix(self, start_node: int) -> list:
        """
        Performs an iterative DFS on the adjacency matrix representation of the graph.

        Args:
            start_node (int): The starting node for DFS.

        Returns:
            list: A list of nodes in the order they are visited.
        """
        visited = set()
        dfs_order = []
        stack = [start_node - 1]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                dfs_order.append(node + 1)

                for neighbor in range(self.graph_size - 1, -1, -1):
                    if neighbor not in visited:
                        if self.adjacency_matrix[node][neighbor] == 1:
                            stack.append(neighbor)

        return dfs_order

    def calculate_diameter(self) -> int:
        """Calculates the diameter of the graph.

        Returns:
            int: The diameter of the graph.
        """
        if self.is_weighted:
            print("Graph is weighted, please use Djikstra.")
            return -1

        if self.adjacency_list is None:
            print("Adjacency list is not initialized.")
            return -1

        diameter = 0

        for node in self.adjacency_list:
            farthest_distance = -1
            for target_node in self.adjacency_list:
                if node != target_node:
                    distance = self.bfs_shortest_path(node, target_node)
                    farthest_distance = max(farthest_distance, distance)
            diameter = max(diameter, farthest_distance)

        return diameter

    def bfs_shortest_path(self, start_node: int, target_node: int) -> int:
        """Finds the shortest path between two nodes in an unweighted graph.

        Args:
            start_node (int): The node from which to start BFS.
            target_node (int): The node to find the shortest path to.

        Returns:
            int: The shortest path distance, or -1 if the target is not reachable.
        """
        if self.is_weighted:
            print("Graph is weighted, please use Djikstra.")
            return -1
        if start_node == target_node:
            return 0

        visited = set()
        queue = [(start_node, 0)]

        visited.add(start_node)

        while queue:
            current_node, distance = queue[0]
            queue = queue[1:]

            for neighbor in self.adjacency_list[current_node]:
                if neighbor == target_node:
                    return distance + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))

        return -1

    def calculate_approximate_diameter(self, sample_size: int) -> int:
        """Estimates the diameter of the graph using a sampling method.

        Args:
            sample_size (int): The number of nodes to sample for diameter estimation.

        Returns:
            int: The estimated diameter of the graph.
        """
        if self.is_weighted:
            print("Graph is weighted, please use Djikstra.")
            return -1

        if self.adjacency_list is None:
            print("Adjacency list is not initialized.")
            return -1

        nodes = list(self.adjacency_list.keys())
        sample = random.sample(nodes, min(sample_size, len(nodes)))
        max_distance = 0

        for node in sample:
            for target in sample:
                if node != target:
                    distance = self.bfs_shortest_path(node, target)
                    max_distance = max(max_distance, distance)

        return max_distance

    def find_connected_components(self) -> dict:
        """Finds all connected components in the graph and returns
        the number of connected components, their sizes, and the nodes in each component.
        Components are listed in descending order of size.

        Returns:
            dict: A dictionary with component sizes and the list of nodes for each component.
                  Format: {size: [list of nodes], ...}
        """
        visited = set()
        components = []

        for node in self.adjacency_list:
            if node not in visited:
                component = self._bfs_component(node, visited)
                components.append(component)

        components.sort(key=len, reverse=True)

        result = {len(component): component for component in components}

        # print(f"Number of connected components: {len(components)}")
        # for size, nodes in result.items():
        #     print(f"Component of size {size}: {nodes}")

        return result

    def _bfs_component(self, start_node: int, visited: set) -> list:
        """Finds all nodes in the current connected component.

        Args:
            start_node (int): The node from which to start BFS.
            visited (set): The set of visited nodes.

        Returns:
            list: The list of nodes in the connected component.
        """
        queue = [start_node]
        component = []
        visited.add(start_node)

        while queue:
            node = queue[0]
            queue = queue[1:]
            component.append(node)

            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return component

    def dijkstra(self, start_node: int, heap: bool = False):
        if self.has_negative_weight:
            return -1

        if heap:
            return self._dijkstra_heap(start_node)

        parents = [start_node] * self.graph_size
        S = set()
        dist = [1e7] * self.graph_size
        dist[start_node - 1] = 0

        while len(S) != self.graph_size:
            min_dist = 1e7
            u = 0
            for i in range(self.graph_size):
                if i in S:
                    continue

                if dist[i] < min_dist:
                    min_dist = dist[i]
                    u = i

            S.add(u)
            for v in self.adjacency_list[u + 1]:
                if dist[v - 1] > dist[u] + self.adjacency_list[u + 1][v]:
                    dist[v - 1] = dist[u] + self.adjacency_list[u + 1][v]
                    parents[v - 1] = u + 1

        return dist, parents

    def _dijkstra_heap(self, start_node: int):
        s = set()
        dist = [float("inf")] * self.graph_size
        dist[start_node - 1] = 0
        parents = [start_node] * self.graph_size

        queue = [(0, start_node)]
        heapify(queue)

        while queue:
            current_dist, current_node = heappop(queue)

            if current_node in s:
                continue

            s.add(current_node)

            for v in self.adjacency_list[current_node]:
                aux = current_dist + self.adjacency_list[current_node][v]
                if dist[v - 1] > aux:
                    dist[v - 1] = aux
                    heappush(queue, (aux, v))
                    parents[v - 1] = current_node

        return dist, parents
