import sys
import plot_graph
import dfs_graph

def main():
    print("\nCosa vuoi fare?")
    print("1) Stampare il grafo (vecchio codice)")
    print("2) Eseguire la DFS e stampare i sottografi (nuovo codice)")
    scelta = input("\nInserisci il numero dell'operazione desiderata: ")

    if scelta == "1":
        plot_graph.main()
    elif scelta == "2":
        dfs_graph.main()
    else:
        print("Scelta non valida. Uscita dal programma.")

if __name__ == "__main__":
    main()
