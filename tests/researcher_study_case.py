import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import Graph

def read_colab_network(filename: str) -> Graph:
    researcher_graph = Graph()
    researcher_graph.initialize_graph_from_txt(file_name=filename, representation="Adjacency List", weighted=True)
    return researcher_graph

def read_colab_network_labels(filename: str) -> dict:
    label_dict = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            node, name = line.strip().split(",")
            label_dict[name] = int(node)
    return label_dict

def match_researcher_to_node(researcher: str, label_dict: dict) -> int:
    try:
        return label_dict[researcher]
    except KeyError:
        print(f"Researcher '{researcher}' not found.")
        return -1

def match_node_to_researcher(node: int, label_dict: dict) -> int:
    for name, node_id in label_dict.items():
        if node_id == node:
            return name
    print(f"Node '{node}' not found.")
    return -1  

def find_researcher_shortest_path(distances: list, parents: list, origin_node: int, destination_node: int, label_dict: dict) -> list:
    if distances[destination_node - 1] == float("inf"):
        print(f"No path from node {origin_node} to node {destination_node}")
        return []

    shortest_path = []
    current_node = destination_node
    while current_node != origin_node:
        shortest_path.append(match_node_to_researcher(current_node, label_dict))
        current_node = parents[current_node - 1]
    shortest_path.append(match_node_to_researcher(origin_node, label_dict))
    shortest_path.reverse()
    return shortest_path

if __name__ == "__main__":
    colab_filename = os.path.join("data", "part_2", "rede_colaboracao.txt")
    colab_label_filename = os.path.join("data", "part_2", "rede_colaboracao_vertices.txt")

    graph = read_colab_network(filename=colab_filename)
    lbl_dict = read_colab_network_labels(filename=colab_label_filename)
    orig_node = match_researcher_to_node("Edsger W. Dijkstra", lbl_dict)
    start_time = time.time()
    dists, prnts = graph.dijkstra(orig_node, heap=True)

    researchers = [
        "Alan M. Turing",
        "J. B. Kruskal",
        "Jon M. Kleinberg",
        "Éva Tardos",
        "Daniel R. Figueiredo"
    ]

    paths = {}
    for rsrchr in researchers:
        dest_node = match_researcher_to_node(researcher=rsrchr, label_dict=lbl_dict)
        paths[rsrchr] = find_researcher_shortest_path(
            distances=dists,
            parents=prnts,
            origin_node=orig_node,
            destination_node=dest_node,
            label_dict=lbl_dict
        )

    total_time = time.time() - start_time

    for rsrchr, path in paths.items():
        print(f"Path to {rsrchr}: {path}")

    print(f"Algorithm runtime: {total_time:.4f} seconds")
