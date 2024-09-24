import statistics
import numpy as np

class Graph:
    """
    Represents a graph that can be initialized from a source file
    and supports adjacency matrix and adjacency list representations.
    Also calculates node degrees, mean, median, and saves graph info to a file.
    """
    
    def __init__(self) -> None:
        """
        Initializes the graph with default attributes.
        """
        self.graph_size = 0
        self.graph_links = []
        self.node_degrees = {}
        self.mean_grade = 0
        self.median_grade = 0
        self.min_degree = None
        self.max_degree = None
        self.adjacency_matrix = None
        self.adjacency_list = {}

    def initialize_graph_from_txt(self, file_name: str, representation: str) -> None:
        """
        Initializes the graph from a text file.

        Args:
            file_name (str): Name of the file containing the graph edges.
            representation (str): Graph representation type ('Adjacency Matrix' or 'Adjacency List').
        """
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                self.graph_size = int(file.readline().strip())
                self.graph_links = []
                
                if representation == "Adjacency Matrix":
                    self.adjacency_matrix = np.zeros((self.graph_size, self.graph_size), dtype=int)
                elif representation == "Adjacency List":
                    self.adjacency_list = {i: [] for i in range(1, self.graph_size + 1)}
                else:
                    raise ValueError(f"Unsupported representation: {representation}")

                for line in file.readlines():
                    link_data = list(map(int, line.split())) 
                    if len(link_data) == 2:
                        u_node, v_node = link_data
                        self.graph_links.append((u_node, v_node))
                        
                        self.node_degrees[u_node] = self.node_degrees.get(u_node, 0) + 1
                        self.node_degrees[v_node] = self.node_degrees.get(v_node, 0) + 1
                        
                        if representation == "Adjacency Matrix":
                            self.adjacency_matrix[u_node - 1][v_node - 1] = 1
                            self.adjacency_matrix[v_node - 1][u_node - 1] = 1
                        elif representation == "Adjacency List":
                            self.adjacency_list[u_node].append(v_node)
                            self.adjacency_list[v_node].append(u_node)
                    else:
                        print(f"Invalid node data: {line.strip()}")
                
                self._calculate_node_metrics()

        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    def _calculate_node_metrics(self) -> None:
        """
        Calculates the min, max, mean, and median degrees of the graph's nodes.
        """
        if self.node_degrees:
            degrees = list(self.node_degrees.values())
            self.min_degree = min(degrees)
            self.max_degree = max(degrees)
            self.mean_grade = sum(degrees) / len(degrees)
            self.median_grade = statistics.median(degrees)

    def write_info_file(self, filename: str) -> None:
        """
        Writes the graph's statistical information to a file.

        Args:
            filename (str): The file to save the graph information.
        """
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Graph Size: {self.graph_size}\n")
            file.write(f"Number of Edges: {len(self.graph_links)}\n")
            file.write(f"Min Degree: {self.min_degree}\n")
            file.write(f"Max Degree: {self.max_degree}\n")
            file.write(f"Mean Degree: {self.mean_grade}\n")
            file.write(f"Median Degree: {self.median_grade}\n")

    def bfs(self, start_node: int, representation: str = "Adjacency List") -> list:
        """
        Chooses the appropriate BFS method based on the representation type.

        Args:
            start_node (int): The node from which to start BFS.
            representation (str): The representation to use ('Adjacency Matrix' or 'Adjacency List').
        
        Returns:
            list: A list of nodes in the order they are visited.
        """
        if representation == "Adjacency List":
            return self.bfs_adjacency_list(start_node)
        elif representation == "Adjacency Matrix":
            return self.bfs_adjacency_matrix(start_node)
        else:
            print(f"Unsupported representation: {representation}")
            return []

    def bfs_adjacency_list(self, start_node: int) -> list:
        """
        Performs BFS using the adjacency list representation.

        Args:
            start_node (int): The node from which to start BFS.
        
        Returns:
            list: A list of nodes in the order they are visited.
        """
        if not self.adjacency_list:
            print("Adjacency list is not initialized.")
            return []

        if start_node not in self.adjacency_list:
            print(f"Start node {start_node} is not in the graph.")
            return []
        
        visited = set()
        bfs_order = []
        queue = [start_node]

        visited.add(start_node)

        while queue:
            current_node = queue.pop(0)
            bfs_order.append(current_node)

            for neighbor in self.adjacency_list[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return bfs_order

    def bfs_adjacency_matrix(self, start_node: int) -> list:
        """
        Performs BFS using the adjacency matrix representation.

        Args:
            start_node (int): The node from which to start BFS.
        
        Returns:
            list: A list of nodes in the order they are visited.
        """
        if self.adjacency_matrix is None:
            print("Adjacency matrix is not initialized.")
            return []
        
        if start_node < 1 or start_node > self.graph_size:
            print(f"Start node {start_node} is not in the valid node range.")
            return []
        
        visited = set()
        bfs_order = []
        queue = [start_node - 1]

        visited.add(start_node - 1)

        while queue:
            current_node = queue.pop(0)
            bfs_order.append(current_node + 1)

            for neighbor in range(self.graph_size):
                if self.adjacency_matrix[current_node][neighbor] == 1 and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return bfs_order

    def calculate_diameter(self) -> int:
        """
        Calculates the diameter of the graph by iterating through every node. 

        Returns:
            int: The diameter of the graph.
        """
        if not self.adjacency_list:
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
        """
        Performs BFS to find the shortest path between two nodes in an unweighted graph.

        Args:
            start_node (int): The node from which to start BFS.
            target_node (int): The node to find the shortest path to.

        Returns:
            int: The shortest path distance, or -1 if the target is not reachable.
        """
        if not self.adjacency_list:
            print("Adjacency list is not initialized.")
            return -1

        if start_node == target_node:
            return 0
        
        visited = set()
        queue = [(start_node, 0)]
        
        visited.add(start_node)
        
        while queue:
            current_node, distance = queue.pop(0)
            
            for neighbor in self.adjacency_list[current_node]:
                if neighbor == target_node:
                    return distance + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return -1

    def find_connected_components(self) -> dict:
        """
        Finds all connected components in the graph using BFS and returns
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

        print(f"Number of connected components: {len(components)}")
        for size, nodes in result.items():
            print(f"Component of size {size}: {nodes}")

        return result
    
    def _bfs_component(self, start_node: int, visited: set) -> list:
        """
        Performs BFS to find all nodes in the current connected component.
        
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
            node = queue.pop(0)
            component.append(node)
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return component
    