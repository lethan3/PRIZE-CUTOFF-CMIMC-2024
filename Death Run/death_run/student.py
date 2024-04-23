import networkx as nx
import random

INF = 1e9 + 7
from networkx import shortest_path_length, has_path


class BaseStudent:
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
            current_vertex: int,
    ) -> int:
        """
        :param edge_updates: A dictionary where the key is an edge (u, v) and the value is how much that edge's weight increased in the current round.
        Note that this only contains information about edge updates in the current round, and not previous rounds.
        :param vertex_count: A dictionary where the key is a vertex and the value is how many students are currently on that vertex.
        :param current_vertex: The vertex that you are currently on.
        :return: The label of the vertex to move to. The edge (current_vertex, next_vertex) must exist.
        """
        pass


# Starter strategy
class RandomStudent(BaseStudent):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take a random out-edge
        v = random.choice(
            [
                x
                for (_, x, _) in filter(
                lambda z: z[0] == current_vertex, self.edge_list
            )
            ]
        )
        w = [
                x
                for (_, _, x) in filter(
                lambda z: z[0] == current_vertex and z[1] == v, self.edge_list
            )
            ][0]
        print("random", v, w)
        return v

class Greedy2Student(BaseStudent):

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take the edge corresponding to the shortest path to any end vertex
        self.process_updates(edge_updates)
        glob_mn = INF
        fin_vert = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = INF
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, adj_vert, p))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight']:
                    fin_vert = adj_vert
        return fin_vert

class GreedyStudent(BaseStudent):

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take the edge corresponding to the shortest path to any end vertex
        self.process_updates(edge_updates)
        glob_mn = INF
        fin_vert = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = INF
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, adj_vert, p))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight']:
                    fin_vert = adj_vert
        return fin_vert


class RandomGreedyStudent(BaseStudent):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take the shortest edge available
        self.process_updates(edge_updates)
        glob_mn = INF
        fin_vert = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            if glob_mn > self.G[current_vertex][adj_vert]['weight']:
                glob_mn = self.G[current_vertex][adj_vert]['weight']
                fin_vert = adj_vert
        print("random_greed", glob_mn, fin_vert)
        return fin_vert

class SmarterGreedyStudent(BaseStudent):

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take the edge corresponding to the shortest path to any end vertex
        self.process_updates(edge_updates)
        glob_mn = INF
        fin_vert = 0
        fin_deg = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = INF
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, adj_vert, p))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight']:
                    if fin_deg <= len(list(self.G.neighbors(adj_vert))):
                        fin_deg = len(list(self.G.neighbors(adj_vert)))
                        fin_vert = adj_vert
        return fin_vert

class PatientGreedyStudent(BaseStudent):

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take the edge corresponding to the shortest path to any end vertex
        self.process_updates(edge_updates)

        #otherwise pick greedily
        glob_mn = INF
        fin_vert = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = INF
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, adj_vert, p))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (current_vertex != 0 or random.randint(0,3) == 0):
                    fin_vert = adj_vert
        return fin_vert


class AvoidantGreedyStudent(BaseStudent):

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)

    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # Take the edge corresponding to the shortest path to any end vertex
        self.process_updates(edge_updates)
        if vertex_count[current_vertex] > 1 or current_vertex == 0:
            return random.choice(
            [
                x
                for (_, x, _) in filter(
                lambda z: z[0] == current_vertex, self.edge_list
            )
            ]
        )
        #otherwise pick greedily (in an intelligent manner)
        glob_mn = INF
        fin_vert = 0
        fin_deg = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = INF
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, adj_vert, p))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight']:
                    if fin_deg <= len(list(self.G.neighbors(adj_vert))):
                        fin_deg = len(list(self.G.neighbors(adj_vert)))
                        fin_vert = adj_vert
        return fin_vert