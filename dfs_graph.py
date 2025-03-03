import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def main():
    # Flag per mostrare o meno i nodi/archi "added"
    SHOW_ADDED = False
    folder_path = "/Users/riccardotortorelli/Desktop/Tesi impronte digitali/Archivio"

    # Verifica che la cartella esista
    if not os.path.exists(folder_path):
        print("Errore: La cartella specificata non esiste.")
        return

    # Lista le impronte disponibili nella cartella
    impronte_disponibili = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

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
            scelta = int(input("\nSeleziona il numero dell'impronta che vuoi visualizzare con DFS: ")) - 1
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
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(15, 12))

    # Disegna il grafo originale in grigio chiaro
    nx.draw(G, pos, node_color="lightgray", edge_color="lightgray", with_labels=True,
            node_size=30, font_size=2)

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
    dfs_image_output_folder = "/Users/riccardotortorelli/Desktop/Tesi/DfsVisit"
    os.makedirs(dfs_image_output_folder, exist_ok=True)

    dfs_image_path = os.path.join(dfs_image_output_folder, f"dfs_{impronta_selezionata}.png")
    plt.savefig(dfs_image_path, dpi=800)
    plt.close()

    print(f"\nImmagine della DFS salvata come: {dfs_image_path}")

    # Stampa l'ordine di visita dei nodi per ogni componente connessa
    print("\nOrdine di visita DFS per ogni componente connessa:")
    for idx, path in enumerate(dfs_paths):
        print(f"Componente {idx+1}: {path}")

# Esegue la funzione main() se il file è eseguito direttamente
if __name__ == "__main__":
    main()
