# shortest_path.py

import os
import json
import math
import networkx as nx
import matplotlib.pyplot as plt

def load_fingerprint_graph(folder_path, impronta_nome):
    """
    Carica il grafo a partire da nodes_graph.json e edges_graph.json.
    Ritorna l'oggetto Graph di NetworkX.
    """
    impronta_path = os.path.join(folder_path, impronta_nome)
    nodes_file = os.path.join(impronta_path, "nodes_graph.json")
    edges_file = os.path.join(impronta_path, "edges_graph.json")

    # Controllo esistenza file
    if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
        print(f"Errore: non trovo {nodes_file} o {edges_file}")
        return None

    # Carico JSON
    with open(nodes_file, 'r') as nf:
        nodes_data = json.load(nf)
    with open(edges_file, 'r') as ef:
        edges_data = json.load(ef)

    nodes = nodes_data['nodes']
    edges = edges_data['edges']

    # Creo il grafo
    G = nx.Graph()

    # Aggiungo nodi
    for i, node in enumerate(nodes):
        pos = tuple(node.get('coordinates', [0, 0]))
        ntype = node.get('type', 'unknown')
        G.add_node(i, pos=pos, type=ntype)

    # Aggiungo archi
    for edge in edges:
        node1, node2 = edge['nodes']
        etype = edge.get('type', 'edge')
        dist  = edge.get('distance', None)  # 'distance' se presente

        # Attenzione a indici di nodo validi
        if node1 < len(nodes) and node2 < len(nodes):
            G.add_edge(node1, node2, type=etype, distance=dist)
        else:
            print(f"Arco {edge['nodes']} non valido.")

    return G

def cost_function_1(u, v, attrs):
    """
    Costo = 1 se arco 'added', altrimenti 0.0001.
    Se l'arco è 'border', decidi come comportarti (ad es. 0.0001 o skip).
    """
    edge_type = attrs.get('type', 'ridge')

    if edge_type == 'added':
        return 1
    elif edge_type == 'border':
        return 2
    else:
        return 0.0001
