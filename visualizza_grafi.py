
# import json
# import networkx as nx
# import matplotlib.pyplot as plt
# import os

# # Flag per mostrare o meno i nodi/archi "added"
# # SHOW_ADDED = False  # Cambia in True se vuoi mostrare anche i nodi e archi "added"
# SHOW_ADDED = False
# # Richiedi il percorso della cartella contenente le impronte
# # folder_path = input("Inserisci il percorso della cartella contenente le impronte digitali: ")
# folder_path = "/Users/riccardotortorelli/Desktop/Tesi/Archivio"

# # Verifica che la cartella esista
# if not os.path.exists(folder_path):
#     print("Errore: La cartella specificata non esiste.")
#     exit()

# # Lista le impronte disponibili nella cartella
# impronte_disponibili = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

# # Se non ci sono impronte disponibili, esci
# if not impronte_disponibili:
#     print("Nessuna impronta trovata nella cartella specificata.")
#     exit()

# # Mostra l'elenco delle impronte disponibili e fai scegliere l'utente
# print("\nImpronte disponibili:")
# for idx, nome in enumerate(impronte_disponibili):
#     print(f"{idx + 1}. {nome}")

# # Selezione dell'impronta da analizzare
# while True:
#     try:
#         scelta = int(input("\nSeleziona il numero dell'impronta che vuoi visualizzare: ")) - 1
#         if 0 <= scelta < len(impronte_disponibili):
#             impronta_selezionata = impronte_disponibili[scelta]
#             break
#         else:
#             print("Selezione non valida, inserisci un numero corretto.")
#     except ValueError:
#         print("Errore: inserisci un numero valido.")

# # Percorso della cartella dell'impronta selezionata
# impronta_path = os.path.join(folder_path, impronta_selezionata)

# # Percorsi ai file JSON
# nodes_file = os.path.join(impronta_path, "nodes_graph.json")
# edges_file = os.path.join(impronta_path, "edges_graph.json")

# # Controllo se i file esistono
# if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
#     print(f"Errore: File nodes_graph.json o edges_graph.json non trovati in {impronta_path}.")
#     exit()

# # Carica i dati dai file JSON
# with open(nodes_file, 'r') as f:
#     nodes_data = json.load(f)
# with open(edges_file, 'r') as f:
#     edges_data = json.load(f)

# nodes = nodes_data['nodes']
# edges = edges_data['edges']

# # Crea un grafo NetworkX
# G = nx.Graph()

# # Aggiunge i nodi con attributi (coordinate e tipo)
# for i, node in enumerate(nodes):
#     pos = tuple(node.get('coordinates', [0, 0]))
#     ntype = node.get('type', 'unknown')
#     G.add_node(i, pos=pos, type=ntype)

# # Aggiunge gli archi con attributi (tipo e distanza, se presenti)
# for edge in edges:
#     node1, node2 = edge['nodes']
#     etype = edge.get('type', 'edge')
#     dist = edge.get('distance', None)
#     # Controlla che gli indici siano validi
#     if node1 < len(nodes) and node2 < len(nodes):
#         G.add_edge(node1, node2, type=etype, distance=dist)
#     else:
#         print(f"Attenzione: arco con nodi {edge['nodes']} non valido.")

# # Ottieni le posizioni dai nodi
# pos = nx.get_node_attributes(G, 'pos')

# # Mappa dei colori per i nodi in base al loro tipo
# node_color_map = {
#     'ending': 'green',
#     'bifurcation': 'blue',
#     'border': 'purple'
# }
# # Mappa dei colori per gli archi in base al tipo
# edge_color_map = {
#     'ridge': 'blue',
#     'border': 'purple'
# }

# # Filtra i nodi e gli archi in base al flag SHOW_ADDED
# if not SHOW_ADDED:
#     # Escludi i nodi di tipo "added"
#     nodes_to_draw = [n for n, attr in G.nodes(data=True) if attr.get('type') != 'added']
#     pos_filtered = {n: pos[n] for n in nodes_to_draw}
#     node_colors = [node_color_map.get(G.nodes[n].get('type'), 'red') for n in nodes_to_draw]
#     # Filtra gli archi: tipo diverso da "added" e entrambi i nodi presenti in nodes_to_draw
#     edges_to_draw = [(u, v) for u, v, attr in G.edges(data=True)
#                      if attr.get('type') != 'added' and u in pos_filtered and v in pos_filtered]
#     edge_colors = [edge_color_map.get(attr.get('type'), 'red') 
#                    for u, v, attr in G.edges(data=True)
#                    if attr.get('type') != 'added' and u in pos_filtered and v in pos_filtered]
# else:
#     nodes_to_draw = list(G.nodes())
#     pos_filtered = pos
#     node_colors = [node_color_map.get(G.nodes[n].get('type'), 'red') for n in G.nodes()]
#     edges_to_draw = [(u, v) for u, v, attr in G.edges(data=True)]
#     edge_colors = [edge_color_map.get(attr.get('type'), 'red') for u, v, attr in G.edges(data=True)]

# # Disegna il grafo
# plt.figure(figsize=(15, 12))
# nx.draw_networkx_nodes(G, pos_filtered, nodelist=nodes_to_draw, node_color=node_colors, node_size=5)
# nx.draw_networkx_edges(G, pos_filtered, edgelist=edges_to_draw, edge_color=edge_colors, width=0.5)
# nx.draw_networkx_labels(G, pos_filtered, labels={n: n for n in nodes_to_draw}, font_size=1, font_color='black')

# plt.axis('off')
# plt.tight_layout()
# plt.savefig(f"{impronta_selezionata}_graph.png", dpi=800)
# plt.show()

import json
import networkx as nx
import matplotlib.pyplot as plt
import os

# Flag per mostrare o meno i nodi/archi "added"
SHOW_ADDED = False
folder_path = "/Users/riccardotortorelli/Desktop/Tesi impronte digitali/Archivio"

# Verifica che la cartella esista
if not os.path.exists(folder_path):
    print("Errore: La cartella specificata non esiste.")
    exit()

# Lista le impronte disponibili nella cartella
impronte_disponibili = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

if not impronte_disponibili:
    print("Nessuna impronta trovata nella cartella specificata.")
    exit()

# Mostra l'elenco delle impronte disponibili e fai scegliere l'utente
print("\nImpronte disponibili:")
for idx, nome in enumerate(impronte_disponibili):
    print(f"{idx + 1}. {nome}")

# Selezione dell'impronta da analizzare
while True:
    try:
        scelta = int(input("\nSeleziona il numero dell'impronta che vuoi visualizzare: ")) - 1
        if 0 <= scelta < len(impronte_disponibili):
            impronta_selezionata = impronte_disponibili[scelta]
            break
        else:
            print("Selezione non valida, inserisci un numero corretto.")
    except ValueError:
        print("Errore: inserisci un numero valido.")

# Percorso della cartella dell'impronta selezionata
impronta_path = os.path.join(folder_path, impronta_selezionata)

# Percorsi ai file JSON
nodes_file = os.path.join(impronta_path, "nodes_graph.json")
edges_file = os.path.join(impronta_path, "edges_graph.json")

if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
    print(f"Errore: File nodes_graph.json o edges_graph.json non trovati in {impronta_path}.")
    exit()

# Carica i dati dai file JSON
with open(nodes_file, 'r') as f:
    nodes_data = json.load(f)
with open(edges_file, 'r') as f:
    edges_data = json.load(f)

nodes = nodes_data['nodes']
edges = edges_data['edges']

# Crea un grafo NetworkX
G = nx.Graph()

# Aggiunge i nodi con attributi (coordinate e tipo)
for i, node in enumerate(nodes):
    pos = tuple(node.get('coordinates', [0, 0]))
    ntype = node.get('type', 'unknown')
    G.add_node(i, pos=pos, type=ntype)

# Aggiunge gli archi, evitando gli archi "added"
for edge in edges:
    node1, node2 = edge['nodes']
    etype = edge.get('type', 'edge')
    dist = edge.get('distance', None)

    # Escludiamo archi "added"
    if etype == "added":
        continue

    if node1 < len(nodes) and node2 < len(nodes):
        G.add_edge(node1, node2, type=etype, distance=dist)
    else:
        print(f"Attenzione: arco con nodi {edge['nodes']} non valido.")

# Rimuove nodi "added"
nodes_to_remove = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'added']
G.remove_nodes_from(nodes_to_remove)

# Algoritmo DFS aggiornato
def dfs(graph, start_node, visited, visit_order):
    stack = [start_node]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            visit_order.append(node)

            # Se il nodo è di tipo "border", interrompi la DFS per questa componente
            if graph.nodes[node].get('type') == 'border':
                return

            # Aggiungi i vicini non visitati alla pila
            stack.extend(neighbor for neighbor in graph.neighbors(node) if neighbor not in visited)

# DFS su tutto il grafo, considerando più componenti e fermandosi ai nodi "border"
visited_global = set()
dfs_paths = []

for node in G.nodes:
    if node not in visited_global:
        visit_order = []
        dfs(G, node, visited_global, visit_order)
        dfs_paths.append(visit_order)

# Visualizzazione del grafo con evidenziazione del percorso DFS
plt.figure(figsize=(15, 12))
pos = nx.get_node_attributes(G, 'pos')

# Disegna il grafo originale in grigio chiaro
nx.draw(G, pos, node_color="lightgray", edge_color="lightgray", with_labels=True, node_size=30, font_size=2)

# Colora i nodi e archi visitati dalla DFS
colors = ["red", "blue", "green", "purple", "orange", "brown"]  # Per componenti multiple
for idx, path in enumerate(dfs_paths):
    color = colors[idx % len(colors)]
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=color, node_size=50)
    edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color=color, width=1.2)

plt.axis('off')
plt.title(f"DFS sul Grafo dell'Impronta: {impronta_selezionata} (senza added, con stop ai border)")

# Salvataggio dell'immagine
dfs_image_path = os.path.join('/Users/riccardotortorelli/Desktop/Tesi impronte digitali/view_grafi/DfsVisit' , f"dfs_{impronta_selezionata}.png")
plt.savefig(dfs_image_path, dpi=800)
plt.close()

print(f"\nImmagine della DFS salvata come: {dfs_image_path}")

# Stampa l'ordine di visita dei nodi per ogni componente connessa
print("\nOrdine di visita DFS per ogni componente connessa:")
for idx, path in enumerate(dfs_paths):
    print(f"Componente {idx+1}: {path}")
