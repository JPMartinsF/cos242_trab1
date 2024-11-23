from core.graph_representations import AdjacencyMatrix, AdjacencyList

class GraphIO:
    """Handles file input and output for the graph."""

    @staticmethod
    def load_graph_from_file(file_name: str, representation: str, size: int, weighted: bool):
        if representation == "Adjacency Matrix":
            graph = AdjacencyMatrix(size)
        elif representation == "Adjacency List":
            graph = AdjacencyList(size, weighted)
        else:
            raise ValueError("Unsupported representation type.")

        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                edge_data = line.strip().split()
                if weighted:
                    u, v, weight = int(edge_data[0]), int(edge_data[1]), float(edge_data[2])
                    graph.add_edge(u, v, weight)
                else:
                    u, v = int(edge_data[0]), int(edge_data[1])
                    graph.add_edge(u, v)
        return graph

    @staticmethod
    def save_graph_to_file(filename: str, graph_stats: dict):
        with open(filename, "w", encoding="utf-8") as file:
            for key, value in graph_stats.items():
                file.write(f"{key}: {value}\n")
