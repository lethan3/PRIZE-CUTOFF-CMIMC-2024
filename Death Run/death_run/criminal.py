import networkx as nx
import random


class BaseCriminal:
    def __init__(
        self, edge_list: list[tuple[int, int, int]], begin: int, ends: list[int]
    ) -> None:
        """
        :param edge_list: A list of tuples representing the edge list of the graph. Tuples are of the
        form (u, v, w), where (u, v) specifies that an edge between vertices u and v exist, and w is the
        weight of that edge.
        :param begin: The label of the vertex which students begin on.
        :param ends: A list of labels of vertices that students may end on (i.e. count as a valid exit).
        """
        pass

    def strategy(
        self,
        edge_updates: dict[tuple[int, int], int],
        vertex_count: dict[int, int],
        budget: int,
    ) -> tuple[int, int, int]:
        """
        :param edge_updates: A dictionary where the key is an edge (u, v) and the value is how much that edge's weight increased in the previous round.
        Note that this only contains information about edge updates in the previous round, and not rounds before that.
        :param vertex_count: A dictionary where the key is a vertex and the value is how many students are currently on that vertex.
        :param budget: The remaining budget
        :return: Which edge to attack and by how much. Must be a tuple of the form (u, v, w) where (u, v) represents the edge endpoints
        and w is the increase in edge weight. w must be in the range [0, budget].
        """
        pass


# Starter strategy
class RandomCriminal(BaseCriminal):
    CONST_NUM_NODES = 120
    CONST_NUM_LAYERS = 15
    CONST_NUM_HEIGHT = 8
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def strategy(self, edge_updates, vertex_count, budget):
        # Find a random populated vertex
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )
        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            random.randint(0, budget),
        )

class ConstrainingCriminal(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]
    def strategy(self, edge_updates, vertex_count, budget):
        # Find a random populated vertex
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )
        adj_possible = [(cv, x, vertex_count[cv]/(len(list(filter(lambda z: z[0] == cv, self.edge_list))) + 1)) for (cv, x, w) in filter(lambda z: z[0] in populated_vertices, self.edge_list)]
        edge_chosen = random.choices([(z[0], z[1]) for z in adj_possible], weights=[z[2] for z in adj_possible], k=1)
        # Fill in random out-edge with random weight
        print(edge_chosen)
        return (edge_chosen[0][0], edge_chosen[0][1], random.randint(0, budget))