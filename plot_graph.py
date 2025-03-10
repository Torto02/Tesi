import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def main():
    # Flag per mostrare o meno i nodi/archi "added"
    SHOW_ADDED = True

    # Percorso della cartella contenente le impronte
    folder_path = "/Users/riccardotortorelli/Desktop/Tesi/Archivio"

    # Verifica che la cartella esista
    if not os.path.exists(folder_path):
        print("Errore: La cartella specificata non esiste.")
        return

    # Lista le impronte disponibili nella carte lla
    impronte_disponibili = sorted([d for d in os.listdir(folder_path)
                               if os.path.isdir(os.path.join(folder_path, d))])

    # Se non ci sono impronte disponibili, esci
    if not impronte_disponibili:
        print("Nessuna impronta trovata nella cartella specificata.")
        return

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

    # Controllo se i file esistono
    if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
        print(f"Errore: File nodes_graph.json o edges_graph.json non trovati in {impronta_path}.")
        return

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

    # Aggiunge gli archi con attributi (tipo e distanza, se presenti)
    for edge in edges:
        node1, node2 = edge['nodes']
        etype = edge.get('type', 'edge')
        dist = edge.get('distance', None)
        # Controlla che gli indici siano validi
        if node1 < len(nodes) and node2 < len(nodes):
            G.add_edge(node1, node2, type=etype, distance=dist)
        else:
            print(f"Attenzione: arco con nodi {edge['nodes']} non valido.")

    # Ottieni le posizioni dai nodi
    pos = nx.get_node_attributes(G, 'pos')

    # Mappa dei colori per i nodi in base al loro tipo
    node_color_map = {
        'ending': 'green',
        'bifurcation': 'blue',
        'border': 'purple'
    }
    # Mappa dei colori per gli archi in base al tipo
    edge_color_map = {
        'ridge': 'blue',
        'border': 'purple'
    }

    # Filtra i nodi e gli archi in base al flag SHOW_ADDED
    if not SHOW_ADDED:
        # Escludi i nodi di tipo "added"
        nodes_to_draw = [n for n, attr in G.nodes(data=True) if attr.get('type') != 'added']
        pos_filtered = {n: pos[n] for n in nodes_to_draw}
        node_colors = [node_color_map.get(G.nodes[n].get('type'), 'red') for n in nodes_to_draw]
        # Filtra gli archi: tipo diverso da "added" e entrambi i nodi presenti in nodes_to_draw
        edges_to_draw = [(u, v) for u, v, attr in G.edges(data=True)
                        if attr.get('type') != 'added' and u in pos_filtered and v in pos_filtered]
        edge_colors = [edge_color_map.get(attr.get('type'), 'red')
                    for u, v, attr in G.edges(data=True)
                    if attr.get('type') != 'added' and u in pos_filtered and v in pos_filtered]
    else:
        nodes_to_draw = list(G.nodes())
        pos_filtered = pos
        node_colors = [node_color_map.get(G.nodes[n].get('type'), 'red') for n in G.nodes()]
        edges_to_draw = [(u, v) for u, v, attr in G.edges(data=True)]
        edge_colors = [edge_color_map.get(attr.get('type'), 'red') for u, v, attr in G.edges(data=True)]

    # Disegna il grafo
    plt.figure(figsize=(15, 12))
    nx.draw_networkx_nodes(G, pos_filtered, nodelist=nodes_to_draw, node_color=node_colors, node_size=5)
    nx.draw_networkx_edges(G, pos_filtered, edgelist=edges_to_draw, edge_color=edge_colors, width=0.5)
    nx.draw_networkx_labels(G, pos_filtered, labels={n: n for n in nodes_to_draw}, font_size=1, font_color='black')

    plt.axis('off')
    plt.tight_layout()
    # Salva l'immagine
    plt.savefig(f"{impronta_selezionata}_graph.png", dpi=800)
    # plt.show()

    print(f"\nIl grafo è stato salvato in '{impronta_selezionata}_graph.png' e anche visualizzato a schermo.")

# Esegue la funzione main() se il file è eseguito direttamente
if __name__ == "__main__":
    main()
