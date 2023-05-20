import networkx as nx
import matplotlib.pyplot as plt


def create_graph(type):
    G = {
        "node": [
            {"point": 1, "pred": 0, "depth": 0, "potential": 10},
            {"point": 2, "pred": 1, "depth": 1, "potential": 0},
            {"point": 3, "pred": 1, "depth": 1, "potential": 0},
            {"point": 4, "pred": 1, "depth": 1, "potential": 0},
            {"point": 5, "pred": 3, "depth": 2, "potential": -10},
            {"point": 5, "pred": 4, "depth": 2, "potential": -10},
            {"point": 5, "pred": 2, "depth": 2, "potential": -10}
        ],
        "arc": [
            {"sp": 1, "ep": 2, "cost": 10, "thread": 5},
            {"sp": 1, "ep": 3, "cost": 12, "thread": 3},
            {"sp": 1, "ep": 4, "cost": 6, "thread": 4},
            {"sp": 2, "ep": 5, "cost": 3, "thread": 6},
            {"sp": 3, "ep": 2, "cost": 2, "thread": 2},
            {"sp": 3, "ep": 5, "cost": 7, "thread": 5},
            {"sp": 3, "ep": 4, "cost": 3, "thread": 5},
            {"sp": 4, "ep": 5, "cost": 3, "thread": 6},
        ]
    }
    return G

# Funzione presa online, stampa i dati di ogni iterazione
def print_structure(T, L=None, G=None):
    if G is not None:
        print("=" * 100)
        print("Original graph G")
        print("=" * 100)
        print("NODES")
        for n in G["node"]:
            print(n)

        print("\n")

        print("ARCS")
        for a in G["arc"]:
            print(a)
        print("=" * 100)

        print("\n")

    print("=" * 100)
    print("Spanning tree T")
    print("=" * 100)
    print("NODES")
    for n in T["node"]:
        print(n)

    print("\n")

    print("ARCS")
    for a in T["arc"]:
        print(a)
    print("=" * 100)

    print("\n")

    if (L is not None):
        print("=" * 100)
        print("Lowebound L")
        print("=" * 100)
        print("ARCS")
        for u in L:
            print(u)
        print("=" * 100)

        print("\n")

# Funzione presa online, disegna il grafo con tutti i cambiamenti di flusso per ogni iterazione
def draw_graph(graph, title, name, L=None, entering=None, spanning=None, leaving=None, arcs=None):
    plt.figure(figsize=(9, 9))

    plt.title(title)
    G = nx.DiGraph()
    for node in graph["node"]:
        G.add_node(node["point"], pred=node["pred"], p=node["potential"])
    for arc in graph["arc"]:
        G.add_edge(arc["sp"], arc["ep"], c=arc["cost"], color="black", width=2)

    pos = nx.drawing.layout.circular_layout(G)
    pos_attr = {}
    for n in pos:
        pos_attr[n] = pos[n].copy()
        pos_attr[n][1] += 0.15

    if (spanning is not None):
        for arc in G.edges():
            if (arcs is not None):
                for e in arcs:
                    if (arc[0] == e["sp"] and arc[1] == e["ep"]):
                        G[arc[0]][arc[1]]['color'] = "blue"
            else:
                G[arc[0]][arc[1]]['color'] = "blue"

            if (entering is not None):
                if (arc[0] == entering["sp"] and arc[1] == entering["ep"]):
                    G[arc[0]][arc[1]]['color'] = "green"
                    G[arc[0]][arc[1]]['width'] = 4
                    G[arc[0]][arc[1]]['c'] = entering["cost"]

                elif (leaving is not None):
                    if (arc[0] == leaving["sp"] and arc[1] == leaving["ep"]):
                        G[arc[0]][arc[1]]['color'] = "red"
                        G[arc[0]][arc[1]]['width'] = 4

            if (L is not None):
                for arc_l in L:
                    if (arc[0] == arc_l["sp"] and arc[1] == arc_l["ep"]):
                        G[arc[0]][arc[1]]['color'] = "orange"
                        G[arc[0]][arc[1]]['c'] = arc_l["cost"]

    edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
    width_list = [G[e[0]][e[1]]['width'] for e in G.edges()]

    nx.draw(G, with_labels=True, pos=pos, node_size=1500, node_color="#004080",
            font_color="white", edge_color=edge_color_list, width=width_list)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={
                                 edge: lab["c"] for edge, lab in G.edges.items() if n in pos})
    nx.draw_networkx_labels(G=G, pos=pos_attr, labels={
                            n: lab for n, lab in G.nodes.items() if n in pos})
    plt.savefig("./img/{}".format(name + ".svg"))
    plt.show()
