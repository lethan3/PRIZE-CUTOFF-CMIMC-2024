import networkx as nx
import random
import time

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
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
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
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
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
            if glob_mn >= self.G[current_vertex][adj_vert]['weight']:
                glob_mn = self.G[current_vertex][adj_vert]['weight']
                fin_vert = adj_vert
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
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
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
        #pick greedily unless current vertex is 0, in which case just pick probabilistically among the good choices
        glob_mn = INF
        fin_vert = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = INF
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight'] or (current_vertex == 0 and random.randint(0, 3) == 0):
                    fin_vert = adj_vert
        return fin_vert


class AvoidantGreedyStudent(BaseStudent):
    pos_vals = {}
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
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight']:
                    if fin_deg <= len(list(self.G.neighbors(adj_vert))):
                        fin_deg = len(list(self.G.neighbors(adj_vert)))
                        fin_vert = adj_vert
        return fin_vert

class BigGreedyStudent(BaseStudent):

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
            mx_w = 0
            for p in self.ends:
                if not has_path(self.G, adj_vert, p):
                    continue
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if glob_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                    mx_w = self.G[current_vertex][adj_vert]['weight']
                    fin_vert = adj_vert
        return fin_vert

class SimpleGreedyStudent(BaseStudent):

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
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
            if glob_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                    fin_vert = adj_vert
        if fin_vert == 0:
            cur_mn = INF
            for adj_vert in list(self.G.neighbors(current_vertex)):
                mn = INF
                for p in self.ends:
                    if not has_path(self.G, adj_vert, p):
                        continue
                    mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                    if mn + self.G[current_vertex][adj_vert]['weight'] > glob_mn:
                        cur_mn = min(cur_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if cur_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                        fin_vert = adj_vert
        return fin_vert
class CautiousGreedyStudent(BaseStudent):

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
                mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])
            if glob_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                if fin_deg <= len(list(self.G.neighbors(adj_vert))):
                    fin_deg = len(list(self.G.neighbors(adj_vert)))
                    fin_vert = adj_vert
        if fin_vert == 0:
            cur_mn = INF
            for adj_vert in list(self.G.neighbors(current_vertex)):
                mn = INF
                for p in self.ends:
                    if not has_path(self.G, adj_vert, p):
                        continue
                    mn = min(mn, shortest_path_length(self.G, source=adj_vert, target=p, weight='weight'))
                    if mn + self.G[current_vertex][adj_vert]['weight'] > glob_mn:
                        cur_mn = min(cur_mn, mn + self.G[current_vertex][adj_vert]['weight'])
                if cur_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                    if fin_deg <= len(list(self.G.neighbors(adj_vert))):
                        fin_deg = len(list(self.G.neighbors(adj_vert)))
                        fin_vert = adj_vert
        return fin_vert

class CautiousAvoidantGreedyStudent(BaseStudent):
    GREED_CONST = 0.2
    GREED_CONST_AHEAD = 0.05
    def __init__(self, edge_list, begin, ends):
        self.t = 0
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)
        self.passed = 0
        self.pos_vals = {}
        self.sp = {}
        self.calc_paths()
        self.vc = {}

    def process_updates(self, edge_updates):
        for upd in edge_updates.keys():
            if len(list(self.G.neighbors(upd[0]))) == 1:
                self.passed = 1
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]
            if edge_updates[upd] > 0:
                self.get_possibilities(upd[0], 0, 1)

    def calc_paths(self):
        for x in range(len(self.G.nodes) - 1, -1, -1):
            if x in self.ends:
                self.sp[x] = 0
            else:
                self.sp[x] = min(list([self.G[x][y]['weight'] + self.sp[y] for y in list(self.G.neighbors(x))]))
    def get_possibilities(self, vertex, counter, rewriting):
        # print(vertex, vertex in self.ends)
        if counter > 4:
            return 0
        if not rewriting and vertex in self.pos_vals.keys():
            return self.pos_vals[vertex]
        if vertex in self.ends:
            self.pos_vals[vertex] = 10
            return 10
        glob_mn = INF
        greedy_mn = (INF, 0)
        count_greed = 0
        pos = 0
        for adj_vert in list(self.G.neighbors(vertex)):
            mn = self.sp[adj_vert]
            if greedy_mn[0] == mn:
                count_greed += 1
            elif greedy_mn[0] > mn:
                count_greed = 1
            greedy_mn = min(greedy_mn, (mn, adj_vert))
            glob_mn = min(glob_mn, mn + self.G[vertex][adj_vert]['weight'])
        for adj_vert in list(self.G.neighbors(vertex)):
            cg = self.GREED_CONST_AHEAD if adj_vert == greedy_mn[1] and count_greed == 1 else 0
            mn = self.sp[adj_vert]
            pos += (self.get_possibilities(adj_vert, counter + 1, 0) - cg) / (8 + 2 * (mn + self.G[vertex][adj_vert]['weight'] - glob_mn) * (mn + self.G[vertex][adj_vert]['weight'] - glob_mn))
        self.pos_vals[vertex] = pos
        return pos

    def strategy(self, edge_updates, vertex_count, current_vertex):
        # start = time.time()
        self.vc = vertex_count
        self.process_updates(edge_updates)
        self.calc_paths()
        # Take the edge corresponding to the shortest path to any end vertex
        # start = time.time()
        glob_mn = INF
        fin_verts = []
        greedy_mn = (INF, 0)
        count_greed = 0
        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = self.sp[adj_vert]
            if greedy_mn[0] == mn:
                count_greed += 1
            elif greedy_mn[0] > mn:
                count_greed = 1
            greedy_mn = min(greedy_mn, (mn, adj_vert))
            glob_mn = min(glob_mn, mn + self.G[current_vertex][adj_vert]['weight'])

        for adj_vert in list(self.G.neighbors(current_vertex)):
            mn = self.sp[adj_vert]
            cg = self.vc[current_vertex] * self.GREED_CONST if adj_vert == greedy_mn[1] and count_greed == 1 else 0

            if glob_mn == mn + self.G[current_vertex][adj_vert]['weight'] and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                fin_verts.append((self.get_possibilities(adj_vert, 0, 0) - cg, random.randint(0, 100), adj_vert))

        if len(fin_verts) == 0:
            cur_mn = INF
            for adj_vert in list(self.G.neighbors(current_vertex)):
                mn = self.sp[adj_vert]
                if mn + self.G[current_vertex][adj_vert]['weight'] > glob_mn and (adj_vert in self.ends or len(list(self.G.neighbors(adj_vert))) > 1):
                    cur_mn = min(cur_mn, mn + self.G[current_vertex][adj_vert]['weight'])

            for adj_vert in list(self.G.neighbors(current_vertex)):
                mn = self.sp[adj_vert]
                if cur_mn == mn + self.G[current_vertex][adj_vert]['weight']:
                    fin_verts.append((self.get_possibilities(adj_vert, 0, 0), random.randint(0, 100), adj_vert))
        fin_verts.sort()
        if len(fin_verts) == 0:
            return list(self.G.neighbors(current_vertex))[0]
        # print(fin_verts)
        # print(current_vertex, fin_verts[-1][1])
        # stop = time.time()
        # self.t += stop - start
        # print(self.t)
        return fin_verts[-1][2]