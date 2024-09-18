import statistics

class Graph:
    
    def __init__(self) -> None:
        self.graph_size = 0
        self.graph_links = []
        self.node_degrees = {}
        self.lowest_graded_node = None
        self.highest_graded_node = None
        self.mean_grade = 0
        self.median_grade = 0

    def initialize_graph_from_txt(self, file_name: str) -> None:
        try:
            with open(file_name, "r") as file:
                self.graph_size = int(file.readline().strip())
                self.graph_links = []
                
                for line in file.readlines():
                    link_data = list(map(int, line.split())) 
                    if len(link_data) == 2:
                        source, destination = link_data
                        self.graph_links.append((source, destination))
                        
                        if source not in self.node_degrees:
                            self.node_degrees[source] = 0
                        if destination not in self.node_degrees:
                            self.node_degrees[destination] = 0
                        self.node_degrees[source] += 1
                        self.node_degrees[destination] += 1
                    else:
                        print(f"Invalid link data: {line.strip()}")
                self.min_degree = min(self.node_degrees.values())
                self.max_degree = max(self.node_degrees.values())
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
            degrees = list(self.node_degrees.values())
            self.mean_grade = sum(degrees) / len(degrees)
            self.median_grade = statistics.median(degrees)