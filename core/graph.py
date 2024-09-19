import statistics
import numpy as np

class Graph:
    
    def __init__(self) -> None:
        self.graph_size = 0
        self.graph_links = []
        self.node_degrees = {}
        self.lowest_graded_node = None
        self.highest_graded_node = None
        self.mean_grade = 0
        self.median_grade = 0

    def initialize_graph_from_txt(self, file_name: str, representation: str) -> None:
        try:
            with open(file_name, "r") as file:
                self.graph_size = int(file.readline().strip())
                self.graph_links = []
                
                match representation:
                    case "Adjacency Matrix":
                        self.adjacency_matrix = np.zeros((self.graph_size, self.graph_size), dtype=int)

                for line in file.readlines():
                    link_data = list(map(int, line.split())) 
                    if len(link_data) == 2:
                        u, v = link_data
                        self.graph_links.append((u, v))
                        
                        if u not in self.node_degrees:
                            self.node_degrees[u] = 0
                        if v not in self.node_degrees:
                            self.node_degrees[v] = 0
                        self.node_degrees[u] += 1
                        self.node_degrees[v] += 1
                        self.adjacency_matrix[u - 1][v - 1] = 1
                        self.adjacency_matrix[v - 1][u - 1] = 1  
                    else:
                        print(f"Invalid link data: {line.strip()}")
                self._calculate_node_metrics()
        except FileNotFoundError:
            print(f"The file '{file_name}' was not found.")

    def write_info_file(self, filename: str) -> None:
        with open(filename, "w") as file:
            file.write(f"{self.graph_size}\n")
            file.write(f"{len(self.graph_links)}\n")
            file.write(f"{self.min_degree}\n")
            file.write(f"{self.max_degree}\n")
            file.write(f"{self.mean_grade}\n")
            file.write(f"{self.median_grade}\n")

    def _calculate_node_metrics(self) -> None:
        if self.node_degrees:
            self.min_degree = min(self.node_degrees.values())
            self.max_degree = max(self.node_degrees.values())
            degrees = list(self.node_degrees.values())
            self.mean_grade = sum(degrees) / len(degrees)
            self.median_grade = statistics.median(degrees)