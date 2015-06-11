import networkx as nx
from matplotlib import pyplot as plt

def dijkstra(graph, src, dest, visited=[], distances={}, predecessors={}) -> list:
    if src not in graph:
        raise TypeError("No source in graph")
    if dest not in graph:
        raise TypeError("No target in graph")

    if src == dest:
        path = []
        pred = dest
        while pred is not None:
            path.append(pred)
            pred = predecessors.get(pred, None)
        print("Shortest path: " + str(path) + " cost=" + str(distances[dest]))
        return path
    else:
        if not visited:
            distances[src] = 0

        for neighbour in graph[src]:
            if neighbour not in visited:
                new_distance = distances[src] + graph[src][neighbour]
                if new_distance < distances.get(neighbour, float('inf')):
                    distances[neighbour] = new_distance
                    predecessors[neighbour] = src

        visited.append(src)

        unvisited = {}

        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = min(unvisited, key=unvisited.get)

        dijkstra(graph, x, dest, visited, distances, predecessors)

def create_nested() -> dict:
    n = int(input("How many edges?\n"))
    out = {}

    def inputs() -> (str, str, int):
        string = input("Input edge parameter (eg. 'a b 3')")
        try:
            return string[0], string[1], int(string[2:])
        except ValueError:
            return inputs()

    for i in range(n):
        first, second, length = inputs()
        if first not in out:
            out[first] = {}
        if second not in out:
            out[second] = {}
        out[first][second] = length
        out[second][first] = length
    return out

if __name__ == "__main__":
    graph = {'a': {'c': 1, 'd': 2},
             'b': {'c': 2, 'f': 3},
             'c': {'a': 1, 'd': 1, 'b': 2},
             'd': {'a': 2, 'c': 1, 'g': 1},
             'e': {'c': 3, 'f': 2},
             'f': {'b': 3, 'g': 1},
             'g': {'f': 1, 'd': 1}}

    # graph = create_nested()

    print(str(dijkstra(graph, 'a', 'f')))

    labels = {}
    edge_labels = {}
    for key in graph.keys():
        labels[key] = key
        for i in graph[key]:
            edge_labels[(key, i)] = graph[key][i]

    G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, labels, 2000,)
    nx.draw_networkx_edges(G, pos, width=5.0)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw_networkx_labels(G, pos, labels)

    plt.show()
    # dijkstra(graph, 'a', 'f')