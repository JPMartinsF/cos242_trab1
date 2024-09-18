class Graph:
    
    def __init__(self) -> None:
        self.graph_size = 0
        self.graph_links = []
        self.node_degrees = {}
        self.lowest_graded_node = None
        self.highest_graded_node = None

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
                
                self._calculate_node_grades()
        except FileNotFoundError:
            raise FileNotFoundError
    
    def _calculate_node_grades(self) -> None:
        if self.node_degrees:
            self.lowest_graded_node = min(self.node_degrees, key=self.node_degrees.get)
            self.highest_graded_node = max(self.node_degrees, key=self.node_degrees.get)
