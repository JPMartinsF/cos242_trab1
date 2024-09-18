class Graph:
    
    def __init__(self) -> None:
        self.graph_size = 0
        self.graph_edges = []

    def read_file(self, file_name: str) -> None:
        with open(file_name, "r") as file:
            self.graph_size = int(file.readline())
            for line in file.readlines():
                edge_data = line.split()
                self.graph_edges.append(edge_data)

    