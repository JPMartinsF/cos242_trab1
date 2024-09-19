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
                        print(f"Invalid link data: {line.strip()}")
                
                self._calculate_node_metrics()

        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except ValueError as e:
            print(f"Error: {e}")

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
