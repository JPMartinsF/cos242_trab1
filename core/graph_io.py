from core.graph_representations import AdjacencyMatrix, AdjacencyList
# from core.graph_new import Graph

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
    def save_graph_to_file(filename: str, graph: 'Graph') -> None:
        """Saves graph information to a file.

        Args:
            filename (str): The file to save the graph information.
            graph (Graph): The graph instance to extract information from.
        """
        metrics = graph.get_degree_metrics()
        num_edges = 0

        if isinstance(graph.representation, AdjacencyMatrix):
            matrix = graph.representation.get_representation()
            num_edges = sum(
                1 for i in range(len(matrix)) for j in range(len(matrix[i]))
                if matrix[i][j] != float('inf') and matrix[i][j] != 0) // 2
        elif isinstance(graph.representation, AdjacencyList):
            adj_list = graph.representation.get_representation()
            num_edges = sum(
                len(neighbors) if isinstance(neighbors, list) else len(neighbors.keys())
                for neighbors in adj_list.values()) // 2

        graph_stats = {
            "Graph Size": graph.size,
            "Number of Edges": num_edges,
            "Min Degree": metrics["min_degree"],
            "Max Degree": metrics["max_degree"],
            "Mean Degree": metrics["mean_degree"],
            "Median Degree": metrics["median_degree"],
        }

        # Write stats to the file
        with open(filename, "w", encoding="utf-8") as file:
            for key, value in graph_stats.items():
                file.write(f"{key}: {value}\n")
