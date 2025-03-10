
import os
import json
import networkx as nx
import math
import matplotlib.pyplot as plt

##############################
# 1) Definisci le funzioni per il matching
##############################

def is_cost_similar(cA, cB, threshold=0.2):
    """
    Ritorna True se cA e cB differiscono meno di 'threshold' (relativo).
    """
    if cA == float('inf') and cB == float('inf'):
        return True
    if cA == float('inf') or cB == float('inf'):
        return False

    denom = max(abs(cA), abs(cB), 1e-9)
    diff = abs(cA - cB) / denom
    return diff <= threshold

def match_subgraphs(
    G_A, G_B,
    M1_A, M2_A,
    M1_B, M2_B,
    nodeA, nodeB,
    mapping=None,
    visited_pairs=None,
    cost_threshold=0.2
):
    """
    DFS parallelo: cerca se il nodo 'nodeA' (in G_A) corrisponde a 'nodeB' (in G_B)
    e se i vicini matchano nei costi M1/M2.
    """
    if mapping is None:
        mapping = {}
    if visited_pairs is None:
        visited_pairs = set()

    if (nodeA, nodeB) in visited_pairs:
        return True
    visited_pairs.add((nodeA, nodeB))

    # 1) I tipi dei nodi devono coincidere
    if G_A.nodes[nodeA].get('type') != G_B.nodes[nodeB].get('type'):
        return False

    # 2) Aggiungiamo la coppia al mapping
    if nodeA in mapping and mapping[nodeA] != nodeB:
        return False
    mapping[nodeA] = nodeB

    # 3) Confronto dei vicini con un DFS parallelo
    neighborsA = list(G_A[nodeA])
    neighborsB = list(G_B[nodeB])

    for nA in neighborsA:
        found_match = False
        for nB in neighborsB:
            # già matchato altrove?
            if nB in mapping.values() and mapping.get(nA, None) != nB:
                continue

            # Confronta costi M1
            costA_m1 = M1_A[nodeA][nA]
            costB_m1 = M1_B[nodeB][nB]
            if not is_cost_similar(costA_m1, costB_m1, cost_threshold):
                continue

            # Confronta costi M2
            costA_m2 = M2_A[nodeA][nA]
            costB_m2 = M2_B[nodeB][nB]
            if not is_cost_similar(costA_m2, costB_m2, cost_threshold):
                continue

            # Ricorsione
            if match_subgraphs(G_A, G_B, M1_A, M2_A, M1_B, M2_B,
                               nA, nB, mapping, visited_pairs, cost_threshold):
                found_match = True
                break
        if not found_match:
            return False

    return True


##############################
# 2) Funzioni di supporto
##############################

def single_source_custom_dijkstra(graph, source, weight_func):
    for (u, v) in graph.edges():
        d = graph[u][v]
        d['temp_weight'] = weight_func(u, v, d)
    distances = nx.single_source_dijkstra_path_length(graph, source, weight='temp_weight')
    for (u, v) in graph.edges():
        del graph[u][v]['temp_weight']
    return distances

def get_subgraph_within_radius(G, M3, source_node, radius):
    N = G.number_of_nodes()
    sub_nodes = [j for j in range(N) if M3[source_node][j] <= radius]
    S = G.subgraph(sub_nodes).copy()
    return S

def plot_and_save_subgraph(S, G, source_node, output_folder, filename):
    pos = nx.get_node_attributes(G, 'pos')
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(S, pos, node_size=50, node_color="red")
    nx.draw_networkx_edges(S, pos, edge_color="black", width=1.5)
    if source_node in S:
        nx.draw_networkx_nodes(S, pos, nodelist=[source_node],
                               node_size=100, node_color="green")
    nx.draw_networkx_labels(S, pos, labels={n: str(n) for n in S.nodes()},
                            font_size=8, font_color="black")

    plt.title(f"Sottografo attorno al nodo {source_node}")
    plt.axis("off")

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Immagine del sottografo salvata in: {output_path}")

def save_matrix_to_file(matrix, filename):
    with open(filename, 'w') as f:
        for row in matrix:
            f.write(','.join(map(str, row)) + '\n')

def plot_mapping(S_A, S_B, G_A, G_B, mapping, output_folder, filename):
    """
    Visualizza il mapping tra due sottografi, mostrando le corrispondenze trovate.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot sottografo A
    pos_A = nx.get_node_attributes(G_A, 'pos')
    nx.draw_networkx_nodes(S_A, pos_A, node_size=50, node_color='lightblue', ax=ax1)
    nx.draw_networkx_edges(S_A, pos_A, edge_color='gray', width=1, ax=ax1)
    nx.draw_networkx_labels(S_A, pos_A, labels={n: str(n) for n in S_A.nodes()},
                          font_size=8, font_color="black", ax=ax1)
    
    # Evidenzia i nodi mappati in A
    mapped_nodes_A = list(mapping.keys())
    if mapped_nodes_A:
        nx.draw_networkx_nodes(S_A, pos_A, nodelist=mapped_nodes_A,
                             node_size=100, node_color='red', ax=ax1)
    
    ax1.set_title("Sottografo A")
    ax1.axis('off')
    
    # Plot sottografo B
    pos_B = nx.get_node_attributes(G_B, 'pos')
    nx.draw_networkx_nodes(S_B, pos_B, node_size=50, node_color='lightblue', ax=ax2)
    nx.draw_networkx_edges(S_B, pos_B, edge_color='gray', width=1, ax=ax2)
    nx.draw_networkx_labels(S_B, pos_B, labels={n: str(n) for n in S_B.nodes()},
                          font_size=8, font_color="black", ax=ax2)
    
    # Evidenzia i nodi mappati in B
    mapped_nodes_B = list(mapping.values())
    if mapped_nodes_B:
        nx.draw_networkx_nodes(S_B, pos_B, nodelist=mapped_nodes_B,
                             node_size=100, node_color='red', ax=ax2)
    
    ax2.set_title("Sottografo B")
    ax2.axis('off')
    
    plt.tight_layout()
    
    # Salva l'immagine
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Mapping visualizzato salvato in: {output_path}")
##############################
# 3) Funzione per caricare una singola impronta e calcolare M1, M2, M3
##############################

def load_fingerprint_and_compute(folder_path):
    """
    Carica una singola impronta da folder_path, costruisce G,
    calcola M1, M2, M3 e SALVA le tre matrici in /OutputMatrices/<nomeImpronta>.
    Ritorna (G, M1, M2, M3).
    """

    # Carica i file JSON
    nodes_file = os.path.join(folder_path, "nodes_graph.json")
    edges_file = os.path.join(folder_path, "edges_graph.json")

    if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
        print(f"Errore: File nodes_graph.json o edges_graph.json non trovati in {folder_path}.")
        return None, None, None, None

    with open(nodes_file, 'r') as f:
        nodes_data = json.load(f)
    with open(edges_file, 'r') as f:
        edges_data = json.load(f)

    nodes = nodes_data['nodes']
    edges = edges_data['edges']

    G = nx.Graph()
    for i, node in enumerate(nodes):
        coord = tuple(node.get('coordinates', [0, 0]))
        ntype = node.get('type', 'unknown')
        G.add_node(i, pos=coord, type=ntype)

    for edge in edges:
        node1, node2 = edge['nodes']
        etype = edge.get('type', 'edge')
        dist = edge.get('distance', None)
        if node1 < len(nodes) and node2 < len(nodes):
            G.add_edge(node1, node2, type=etype, distance=dist)
        else:
            print(f"Attenzione: arco con nodi {edge['nodes']} non valido.")

    # Definizione delle 2 funzioni di peso
    def weight_function_m1(u, v, d):
        arco_type = d.get('type')
        if arco_type == 'added':
            return 1.0
        elif arco_type == 'border':
            return 5.0
        else:
            return 0.0001

    def weight_function_m2(u, v, d):
        if d.get('type') == 'added':
            pos_u = G.nodes[u]['pos']
            pos_v = G.nodes[v]['pos']
            return math.dist(pos_u, pos_v)
        else:
            dist_attr = d.get('distance')
            if dist_attr is not None:
                return dist_attr
            else:
                pos_u = G.nodes[u]['pos']
                pos_v = G.nodes[v]['pos']
                return math.dist(pos_u, pos_v)

    N = G.number_of_nodes()

    # Calcolo M1
    M1 = [[float('inf')] * N for _ in range(N)]
    for node_start in G.nodes():
        dist_dict = single_source_custom_dijkstra(G, node_start, weight_function_m1)
        for node_end, dist_val in dist_dict.items():
            M1[node_start][node_end] = dist_val

    # Calcolo M2
    M2 = [[float('inf')] * N for _ in range(N)]
    for node_start in G.nodes():
        dist_dict = single_source_custom_dijkstra(G, node_start, weight_function_m2)
        for node_end, dist_val in dist_dict.items():
            M2[node_start][node_end] = dist_val

    # Calcolo M3
    M3 = [[0.0] * N for _ in range(N)]
    coords = [G.nodes[i]['pos'] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if i == j:
                M3[i][j] = 0.0
            else:
                M3[i][j] = math.dist(coords[i], coords[j])

    # ****** SALVIAMO LE MATRICI in OutputMatrices ******
    out_folder = "/Users/riccardotortorelli/Desktop/Tesi/OutputMatrices"
    impronta_nome = os.path.basename(folder_path)  # nome della cartella dell'impronta
    sub_folder = os.path.join(out_folder, impronta_nome)
    os.makedirs(sub_folder, exist_ok=True)

    save_matrix_to_file(M1, os.path.join(sub_folder, "M1.csv"))
    save_matrix_to_file(M2, os.path.join(sub_folder, "M2.csv"))
    save_matrix_to_file(M3, os.path.join(sub_folder, "M3.csv"))
    print(f"\nM1, M2, M3 salvate in: {sub_folder}")

    return G, M1, M2, M3


##############################
# 4) Funzione principale che carica e confronta due impronte
##############################

def main():
    base_folder = "/Users/riccardotortorelli/Desktop/Tesi/Archivio"
    if not os.path.exists(base_folder):
        print("Errore: La cartella specificata non esiste.")
        return

    # Elenco delle impronte disponibili
    impronte_disponibili = sorted([d for d in os.listdir(base_folder)
                                   if os.path.isdir(os.path.join(base_folder, d))])
    if len(impronte_disponibili) < 2:
        print("Servono almeno 2 impronte nella cartella.")
        return

    # 1) SCELTA IMPRONTA A
    print("\nImpronte disponibili:")
    for idx, nome in enumerate(impronte_disponibili):
        print(f"{idx + 1}. {nome}")

    while True:
        try:
            sceltaA = int(input("\nSeleziona il numero dell'impronta A: ")) - 1
            if 0 <= sceltaA < len(impronte_disponibili):
                improntaA_selezionata = impronte_disponibili[sceltaA]
                break
            else:
                print("Selezione non valida, inserisci un numero corretto per A.")
        except ValueError:
            print("Errore: inserisci un numero valido.")

    folder_A = os.path.join(base_folder, improntaA_selezionata)
    G_A, M1_A, M2_A, M3_A = load_fingerprint_and_compute(folder_A)
    if G_A is None:
        print("Impossibile caricare impronta A.")
        return

    # 2) SCELTA IMPRONTA B
    while True:
        try:
            sceltaB = int(input("\nSeleziona il numero dell'impronta B: ")) - 1
            if 0 <= sceltaB < len(impronte_disponibili) and sceltaB != sceltaA:
                improntaB_selezionata = impronte_disponibili[sceltaB]
                break
            else:
                print("Selezione non valida, inserisci un numero corretto per B (diverso da A).")
        except ValueError:
            print("Errore: inserisci un numero valido.")

    folder_B = os.path.join(base_folder, improntaB_selezionata)
    G_B, M1_B, M2_B, M3_B = load_fingerprint_and_compute(folder_B)
    if G_B is None:
        print("Impossibile caricare impronta B.")
        return

    print(f"\nImpronta A = {improntaA_selezionata}, nodi={G_A.number_of_nodes()}, archi={G_A.number_of_edges()}")
    print(f"Impronta B = {improntaB_selezionata}, nodi={G_B.number_of_nodes()}, archi={G_B.number_of_edges()}")

    # 3) Estrazione sottografo A
    minutieA = [n for n in G_A.nodes() if G_A.nodes[n].get('type') in ('ending','bifurcation')]
    if not minutieA:
        print("Nessuna minuzia trovata in impronta A.")
        return
    minuziaA = minutieA[1368]
    max_dist_A = max(max(row) for row in M3_A if max(row) < float('inf'))
    radiusA = 0.04 * max_dist_A
    S_A = get_subgraph_within_radius(G_A, M3_A, minuziaA, radiusA)

    # 4) Estrazione sottografo B
    minutieB = [n for n in G_B.nodes() if G_B.nodes[n].get('type') in ('ending','bifurcation')]
    if not minutieB:
        print("Nessuna minuzia trovata in impronta B.")
        return
    minuziaB = minutieB[1245]
    max_dist_B = max(max(row) for row in M3_B if max(row) < float('inf'))
    radiusB = 0.1 * max_dist_B
    S_B = get_subgraph_within_radius(G_B, M3_B, minuziaB, radiusB)

    print(f"\nSottografo A con raggio={radiusA:.2f}, nodi={S_A.number_of_nodes()}, archi={S_A.number_of_edges()}")
    print(f"Sottografo B con raggio={radiusB:.2f}, nodi={S_B.number_of_nodes()}, archi={S_B.number_of_edges()}")

    # Se vuoi salvare le immagini dei sottografi:
    out_subgraphs = "/Users/riccardotortorelli/Desktop/Tesi/OutputSubgraphs"
    plot_and_save_subgraph(S_A, G_A, minuziaA, out_subgraphs, f"subgraphA_{minuziaA}.png")
    plot_and_save_subgraph(S_B, G_B, minuziaB, out_subgraphs, f"subgraphB_{minuziaB}.png")

    # # 5) Esegui match_subgraphs
    # mapping = {}
    # success = match_subgraphs(
    #     S_A, S_B,
    #     M1_A, M2_A,
    #     M1_B, M2_B,
    #     minuziaA, minuziaB,
    #     mapping=mapping,
    #     cost_threshold=0.2
    # )
    # if success:
    #     print("\nI sottografi locali matchano correttamente!")
    #     print("Mapping nodo di A -> nodo di B:", mapping)
    # else:
    #     print("\nNessun match trovato per i sottografi locali attorno alle minuzie scelte.")

    # print("\n--- Elaborazione completata ---")
    # 5) Esegui match_subgraphs con tutte le minuzie del sottografo B
    print("\nConfrontando la minuzia A con tutte le minuzie del sottografo B...")
    
    # Ottieni tutte le minuzie nel sottografo B
    minutie_in_S_B = [n for n in S_B.nodes() if S_B.nodes[n].get('type') in ('ending', 'bifurcation')]
    
    if not minutie_in_S_B:
        print("Nessuna minuzia trovata nel sottografo B per il confronto.")
    else:
        match_trovati = 0
        for idx, minuzia_target_B in enumerate(minutie_in_S_B):
            mapping = {}
            success = match_subgraphs(
                S_A, S_B,
                M1_A, M2_A,
                M1_B, M2_B,
                minuziaA, minuzia_target_B,
                mapping=mapping,
                cost_threshold=0.2
            )
            
            if success:
                match_trovati += 1
                print(f"\nMatch #{match_trovati} trovato!")
                print(f"Minuzia A (nodo {minuziaA}) -> Minuzia B (nodo {minuzia_target_B})")
                print("Mapping completo:", mapping)
                
                # Opzionale: visualizza il mapping graficamente
                plot_mapping(S_A, S_B, G_A, G_B, mapping, out_subgraphs, f"mapping_{minuziaA}_{minuzia_target_B}.png")
        
        if match_trovati == 0:
            print("\nNessun match trovato tra la minuzia A e le minuzie del sottografo B.")
        else:
            print(f"\nTotale match trovati: {match_trovati} su {len(minutie_in_S_B)} minuzie testate.")

    print("\n--- Elaborazione completata ---")

if __name__ == "__main__":
    main()
