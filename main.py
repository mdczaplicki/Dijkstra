from matplotlib.pyplot import figure, scatter
import networkx as nx
from matplotlib import pyplot as plt

g_path = []


def dijkstra(graph_in, src, dest, visited=None, distances=None, predecessors=None) -> list:

    if not predecessors:
        predecessors = {}
    if not distances:
        distances = {}
    if not visited:
        visited = []
    global g_path
    if src not in graph_in:
        raise TypeError("No source in graph")
    if dest not in graph_in:
        raise TypeError("No target in graph")

    if src == dest:
        path = []
        pred = dest
        while pred is not None:
            path.append(pred)
            g_path.append(pred)
            pred = predecessors.get(pred, None)
        g_path = g_path[::-1]
        print("Shortest path: " + str(path[::-1]) + " cost " + str(distances[dest]))
        return path
    else:
        if not visited:
            distances[src] = 0

        for neighbour in graph_in[src]:
            if neighbour not in visited:
                new_distance = distances[src] + graph_in[src][neighbour]
                if new_distance < distances.get(neighbour, float('inf')):
                    distances[neighbour] = new_distance
                    predecessors[neighbour] = src

        visited.append(src)

        unvisited = {}

        for k in graph_in:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = min(unvisited, key=unvisited.get)

        dijkstra(graph_in, x, dest, visited, distances, predecessors)


def create_nested() -> dict:
    n = int(input("How many edges?\n"))
    out = {}

    def inputs() -> (str, str, int):
        string = input("Input edge parameter (eg. 'a b 3')")
        try:
            return string[0], string[1], int(string[2:])
        except ValueError:
            return inputs()

    for j in range(n):
        first, second, length = inputs()
        if first not in out:
            out[first] = {}
        if second not in out:
            out[second] = {}
        out[first][second] = length
        out[second][first] = length
    return out

if __name__ == "__main__":
    n = int(input("0. From file\n1. Manually\n"))
    if n == 0:
        graph = {'a': {'c': 1, 'd': 2},
                 'b': {'c': 2, 'f': 3},
                 'c': {'a': 1, 'b': 2, 'd': 1},
                 'd': {'a': 2, 'c': 1, 'g': 1},
                 'e': {'c': 3, 'f': 2},
                 'f': {'b': 3, 'g': 1},
                 'g': {'f': 1, 'd': 1}}
    else:
        graph = create_nested()

    G = nx.Graph(graph)
    fig = figure()

    labels = {}
    edge_labels = {}
    colors = []
    edge_colors = []

    for i in G.nodes():
        labels[i] = i
        for j in graph[i]:
            edge_labels[(i, j)] = graph[i][j]

    def create_attributes():
        global labels, edge_labels, colors, edge_colors
        for k in G.nodes():
            labels[k] = k
            for j in graph[k]:
                edge_labels[(k, j)] = graph[k][j]
            if k in g_path:
                colors.append('red')
            else:
                colors.append('pink')

        for k in G.edges():
            if k[0] in g_path and k[1] in g_path:
                edge_colors.append('blue')
            else:
                edge_colors.append('black')

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, labels, 2000, node_color='pink')
    nx.draw_networkx_edges(G, pos, width=5.0, edge_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw_networkx_labels(G, pos, labels)

    def show_map():
        nx.draw_networkx_nodes(G, pos, labels, 2000, node_color=colors)
        nx.draw_networkx_edges(G, pos, width=5.0, edge_color=edge_colors)
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        nx.draw_networkx_labels(G, pos, labels)

    d_s = ''
    d_f = ''
    d_i = 0

    def on_pick(event):
        global d_i, d_s, d_f
        t = event.ind[0]
        if d_i == 0:
            d_s = G.nodes()[t]
            d_i += 1
        elif d_i == 1:
            d_f = G.nodes()[t]
            plt.cla()
            dijkstra(graph, d_s, d_f)
            create_attributes()
            show_map()
            plt.show()
            d_i = 0
        else:
            pass
        print("Clicked on ", G.nodes()[t])
    scatter(*zip(*pos.values()), alpha=1.0, s=20, picker=True)
    fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()
