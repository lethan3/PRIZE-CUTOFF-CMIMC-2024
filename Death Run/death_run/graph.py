import random
import networkx as nx
import matplotlib.pyplot as plt


def generate_graph(
    dim: tuple[int, int], weight_range: tuple[int, int], path: str | None = None
) -> tuple[list[tuple[int, int, int]], int, list[int]]:
    """Generates a directed acyclic graph with the specified dimensions. The width specifies how many layers to the graph.
    The height specifies the number of vertices in each layer. Vertices between adjacent layers are connected with a
    probability of 1/2. Edges are directed from the previous layer to the next. Each edge is assigned a weight from the
    specified weight range, uniformly. Returns the edge list.

    :param dim: A tuple of the form (width, height), specifying the dimensions of the graph.
    :param weight_range: A tuple of the form (min, max), specifying the minimum and maximum edge weights.
    :param path: An optional string specifying where to save the graph visualiation to. If None, then no visualization.
    :return: A tuple (edge_list, begin, ends), where:
        -  edge_list is a list of tuples representing the edge list of the graph. Tuples are of the form (u, v, w), where
        (u, v) specifies that an edge between vertices u and v exist, and w is the weight of that edge.
        - begin is the vertex that all players begin on.
        - ends is the list of vertices that players may end on.
    """
    (w, h) = dim

    edge_list = []

    prev_layer = [0]
    layers = [prev_layer]
    curr_idx = 1

    for i in range(w):
        curr_layer = [curr_idx + j for j in range(h)]
        curr_idx += h

        if i == 0:
            for x in prev_layer:
                for y in curr_layer:
                    edge_list.append((x, y, random.randint(*weight_range)))
        else:
            for x in prev_layer:
                connected = False

                for y in curr_layer:
                    if random.random() < 0.5:
                        connected = True
                        edge_list.append((x, y, random.randint(*weight_range)))

                if not connected:
                    edge_list.append(
                        (
                            x,
                            random.choice(curr_layer),
                            random.randint(*weight_range),
                        )
                    )

            for x in curr_layer:
                connected = any(y == x for (_, y, _) in edge_list)
                if not connected:
                    edge_list.append(
                        (
                            random.choice(prev_layer),
                            x,
                            random.randint(*weight_range),
                        )
                    )

        prev_layer = curr_layer
        layers.append(prev_layer)

    if path:
        pos = {0: (0, 0)}
        for i in range(1, w + 1):
            mid = layers[i][0] + (h // 2)
            for x in layers[i]:
                pos[x] = (2 * i, mid - x)
        G = edge_list_to_nx(edge_list)
        nx.draw(G, pos, with_labels=True)
        plt.savefig(path)
        plt.close()

    return edge_list, 0, prev_layer


def edge_list_to_nx(edge_list: list[int, int, int]):
    """
    Converts a weighted edge list to a NetworkX graph.

    @param edge_list: A list of tuples representing the edge list of the graph. Tuples are of the
    form (u, v, w), where (u, v) specifies that an edge between vertices u and v exist, and w is the
    weight of that edge.

    @return A NetworkX graph representing the graph specified by edge_list.
    """
    G = nx.DiGraph()
    G.add_weighted_edges_from(edge_list)
    return G
