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

class HotHeadedCriminal(BaseCriminal):
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
        pos_verts = [v for v in filter(lambda z: len(list(self.G.neighbors(z))) == 1, populated_vertices)]
        if len(pos_verts) > 0:
            fin_vert = 0
            vc = 0
            for v in pos_verts:
                if vertex_count[v] > vc:
                    vc = vertex_count[v]
                    fin_vert = v
            return (fin_vert, list(self.G.neighbors(fin_vert))[0], budget)
        print(pos_verts)

        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            0,
        )

class MiffedCriminal(BaseCriminal):
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
        pos_verts = [v for v in filter(lambda z: len(list(self.G.neighbors(z))) <= 3, populated_vertices)]
        if len(pos_verts) > 0:
            fin_vert = 0
            vc = 0
            for v in pos_verts:
                if vertex_count[v] > vc:
                    vc = vertex_count[v]
                    fin_vert = v
            return (fin_vert, list(self.G.neighbors(fin_vert))[0], random.randint(0,budget))
        print(pos_verts)

        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            0,
        )


class CrowdCriminal(BaseCriminal):
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
        # Add to the smallest edge adjacent to a crowded vertex
        populated_vertices = list(
            filter(lambda z: vertex_count[z], vertex_count.keys())
        )
        pos_verts = [v for v in filter(lambda z: len(list(self.G.neighbors(z))) <= 3, populated_vertices)]
        if len(pos_verts) > 0:
            fin_vert = 0
            vc = 0
            for v in pos_verts:
                if vertex_count[v] > vc:
                    vc = vertex_count[v]
                    fin_vert = v
            return (fin_vert, list(self.G.neighbors(fin_vert))[0], random.randint(0,budget))
        print(pos_verts)

        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            0,
        )

class CooldownCriminal(BaseCriminal):
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
        ok = 0
        for v in list(self.G.neighbors(populated_vertices[0])):
            if len(list(self.G.neighbors(v))) == 0:
                ok = 1
        if ok == 1:
            cur = random.choice(populated_vertices)
            return (
                cur,
                random.choice(
                    [x for (_, x, _) in filter(lambda z: z[0] == cur, self.edge_list)]
                ),
                budget
            )
        pos_verts = [v for v in filter(lambda z: len(list(self.G.neighbors(z))) == 1, populated_vertices)]
        if len(pos_verts) > 0:
            fin_vert = 0
            vc = 0
            for v in pos_verts:
                if vertex_count[v] > vc:
                    vc = vertex_count[v]
                    fin_vert = v
            return (fin_vert, list(self.G.neighbors(fin_vert))[0], budget)
        print(pos_verts)

        vertex = random.choice(populated_vertices)
        # Fill in random out-edge with random weight
        return (
            vertex,
            random.choice(
                [x for (_, x, _) in filter(lambda z: z[0] == vertex, self.edge_list)]
            ),
            0,
        )

class AdjustorCriminal(BaseCriminal):
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        # print(edge_list)
        self.G.add_weighted_edges_from(edge_list)
        # print(self.G.edges.data())
    def weight_of_best_path_to_sink(self, current_vertex):
        # print("possible paths from", current_vertex, list([(x, nx.shortest_path_length(self.G, source=current_vertex, target=x, weight='weight')) for x in self.ends if nx.has_path(self.G, current_vertex, x)]))
        return min(list([nx.shortest_path_length(self.G, source=current_vertex, target=x, weight='weight') for x in self.ends if nx.has_path(self.G, current_vertex, x)]))
    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]
    def strategy(self, edge_updates, vertex_count, budget):
        # print("adjustor budget:", budget)
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            vertex_weights = [(self.weight_of_best_path_to_sink(v), v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            # print("vertex_weights", vertex_weights)
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [((v[2] - 1) * v[3], v[2]-1, v[0], v[1]) for v in edge_pos if v[2] - 1 > 0]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            return final_possibilities[-1][2], final_possibilities[-1][3], final_possibilities[-1][1] #take the edge that will maximize short run score
        else:
            return 0, list(self.G.neighbors(0))[0], 0  #skip the turn

class RobinHoodCriminal(BaseCriminal):
    MAX_SPEND = 25
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
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        if vertex_count[0] == 8:
            return (0, random.choice(list([x[1] for x in self.edge_list if x[0] == 0])), 0)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                continue
                # edge_pos.append((cv, vertex_weights[0][1], budget//2, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [((v[2] - 1) * v[3], v[2]-1, v[0], v[1]) for v in edge_pos if v[2] - 1 > 0]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            return final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1]) #take the edge that will maximize short run score
        else:
            vertex = max([(v[3], v[0]) for v in edge_pos])[1]
            # print("making random move", fin)
            return (vertex, random.choice(list([x[1] for x in self.edge_list if x[0] == vertex])), 0)

class AngryRobinHoodCriminal(BaseCriminal):
    MAX_SPEND = 75
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
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        if vertex_count[0] == self.begin:
            return (0, random.choice(list([x[1] for x in self.edge_list if x[0] == self.begin])), 0)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget//2, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [((v[2] - 1) * v[3], v[2]-1, v[0], v[1]) for v in edge_pos if v[2] - 1 > 0]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            return final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1]) #take the edge that will maximize short run score
        else:
            vertex = max([(v[3], v[0]) for v in edge_pos])[1]
            # print("making random move", fin)
            return (vertex, random.choice(list([x[1] for x in self.edge_list if x[0] == vertex])), random.randint(0, min(budget, self.MAX_SPEND)))

class AngryConstrainingRobinHoodCriminal(BaseCriminal):
    MAX_SPEND = 75
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
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget//2 + (budget//2 - 1 if cv_count > 1 else -1), cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [((v[2] - 1) * v[3], v[2]-1, v[0], v[1]) for v in edge_pos if v[2] - 1 > 0]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            fin_choice = final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1]) #take the edge that will maximize short run score
            return fin_choice #take the edge that will maximize short run score
        else:
            return self.begin, list(self.G.neighbors(self.begin))[0], 0 #skip this turn (very unlikely)

class AngryConstrainingCriminal(BaseCriminal):
    MAX_SPEND = 75
    MAX_DEG = 9
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
        print("current budget", budget)
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        if vertex_count[0] == 8:
            fin_ret = (0, random.choice(list([x[1] for x in self.edge_list if x[0] == 0])), 0)
            return fin_ret
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        vertex = max([(v[0] * (self.MAX_DEG - len(list(self.G.neighbors(v[1])))), v[1]) for v in populated_vertices])[1]
        assert(self.G.neighbors(vertex) != 0)

        print("neighbors", list(self.G.neighbors(vertex)))
        end_vert = random.choice(list([x[1] for x in self.edge_list if x[0] == vertex]))
        print("making random move", vertex, end_vert)
        return (vertex, end_vert, random.randint(0, budget if end_vert in self.ends else budget * 3//4))

class EvilAngryConstrainingRobinHoodCriminal(BaseCriminal):
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
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [(v[2] * v[3], v[2], v[0], v[1]) for v in edge_pos]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            fin_choice = final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1])
            # print("evil", fin_choice)
            return fin_choice #take the edge that will maximize short run score
        else:
            vertex = max([(v[3], v[0]) for v in edge_pos])[1]
            # print("making random move", fin)
            fin_choice = (vertex, random.choice(list([x[1] for x in self.edge_list if x[0] == vertex])), 0)
            # print("evil", fin_choice)
            return fin_choice

class PredictiveEvilAngryConstrainingRobinHoodCriminal(BaseCriminal):
    AHEAD_PROB = 17
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)
        self.number_ahead = 0
    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]
    def strategy(self, edge_updates, vertex_count, budget):
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget if cv_count > 1 else budget//2, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [(v[2] * v[3], v[2], v[0], v[1]) for v in edge_pos]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities) and (final_possibilities[-1][1] >= budget//2 or random.randint(1, self.AHEAD_PROB) <= self.AHEAD_PROB - 1):
            # print("final", final_possibilities[-1])
            return final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1]) #take the edge that will maximize short run score
        else:
            # calculate a score based on the expected winnings from each minimum vertex adjacent to a populated vertex
            # assert len(edge_pos) != 0
            min_list = [(x[0], min(list([(self.G[x[1]][v[1]]['weight'], v[1]) for v in self.edge_list if v[0] == x[1]]))[1]) for x in populated_vertices]
            next_pos = []
            for cv_count, cv in min_list:
                if cv in self.ends:
                    continue
                vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
                vertex_weights.sort()
                if len(vertex_weights) == 1:
                    next_pos.append(
                        (cv, vertex_weights[0][1], budget // 2 + (-1 if cv_count < 2 else budget // 2 - 1), cv_count))
                else:
                    next_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
            final_possibilities = [((v[2] + 1) * v[3], v[2] + 1, v[0], v[1]) for v in next_pos if v[2] + 1 > 0]
            final_possibilities.sort()
            # print("final_possibilities", final_possibilities)


            if len(final_possibilities) == 0:
                return self.begin, list(self.G.neighbors(self.begin))[0], 0 #skip this turn (very unlikely)

            #add as much as is reasonable to the second smallest edge

            # print("neighbors", list(self.G.neighbors(vertex)))
            fin_choice = final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1])
            # print("helper move", fin_choice)
            self.number_ahead += 1
            # print(self.number_random)
            return fin_choice

class HybridBetweenEvilAngryConstrainingRobinHoodCriminalAndAngryConstrainingRobinHoodCriminal(BaseCriminal):
    COPIED_THRESHOLD = 2
    TURNS_CONST = 4
    DEPTH_CONST = 9

    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)
        self.number_ahead = 0
        self.num_equal = 0
        self.prev_choice = 0
        self.evil = 1
        self.num_copied = 0
        self.turns = 0
        self.depth = 0
        self.prev_edge = (-1, -1, -1)

    def process_updates(self, edge_updates):
        if self.prev_edge[2] == -1:
            return
        self.depth += 1
        if self.prev_edge[2] > 0:
            self.turns += 1
        if edge_updates[self.prev_edge[0], self.prev_edge[1]] > self.prev_edge[2] and self.turns < self.TURNS_CONST:
            self.num_copied += 1
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]

    def play_evil_angry_constraining_robin_hood(self, edge_updates, vertex_count, budget):
        # print("evil")
        # For each populated vertex, check if there exists a unique
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = []  # start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append(
                    (cv, vertex_weights[0][1], budget if (cv_count > 1 or self.depth >= self.DEPTH_CONST) else budget * 3//5, cv_count))
                self.evil = 0
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [(v[2] * v[3], v[2], v[0], v[1]) for v in edge_pos]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            return final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1])  # take the edge that will maximize short run score
        else:
            vertex = max([(v[3], v[0]) for v in edge_pos])[1]
            # print("making random move", fin)
            return (vertex, random.choice(list([x[1] for x in self.edge_list if x[0] == vertex])), 0)

    def play_angry_constraining_robin_hood(self, edge_updates, vertex_count, budget):
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget-1 if (cv_count > 1 or self.turns > 10) else budget//2-1, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [((v[2] - 1) * v[3], v[2]-1, v[0], v[1]) for v in edge_pos if v[2] - 1 > 0]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            fin_choice = final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1]) #take the edge that will maximize short run score
            return fin_choice #take the edge that will maximize short run score
        else:
            return self.begin, list(self.G.neighbors(self.begin))[0], 0 #skip this turn (very unlikely)

    def strategy(self, edge_updates, vertex_count, budget):
        self.process_updates(edge_updates)
        fin_choice = (-1, -1, -1)
        if self.evil and not (self.turns >= self.TURNS_CONST and self.num_copied < self.COPIED_THRESHOLD):
            fin_choice = self.play_evil_angry_constraining_robin_hood(edge_updates, vertex_count, budget)
        else:
            fin_choice = self.play_angry_constraining_robin_hood(edge_updates, vertex_count, budget)
        self.prev_edge = fin_choice
        return fin_choice

class HeroicAngryConstrainingRobinHoodCriminal(BaseCriminal):
    MAX_SPEND = 75
    PRED_LIM = 3
    PRED_CHECK = 5
    def __init__(self, edge_list, begin, ends):
        self.edge_list = edge_list
        self.begin = begin
        self.ends = ends
        self.G = nx.DiGraph()
        self.G.add_weighted_edges_from(edge_list)
        self.G.predicting = 2
        self.G.spent = 1
    def process_updates(self, edge_updates):
        for upd in edge_updates:
            self.G[upd[0]][upd[1]]['weight'] += edge_updates[upd]
    def upd_pred(self):
        self.G.predicting = (self.G.predicting + self.G.spent) % self.PRED_CHECK
    def strategy(self, edge_updates, vertex_count, budget):
        # print("predicting?", self.G.predicting)
        # For each populated vertex, check if there exists a unique
        self.process_updates(edge_updates)
        populated_vertices = [(vertex_count[z], z) for z in vertex_count.keys() if vertex_count[z] > 0]
        populated_vertices.sort()
        edge_pos = [] #start node, end node, amount of change, number of students on each node
        for cv_count, cv in populated_vertices:
            if cv in self.ends:
                continue
            vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
            vertex_weights.sort()
            if len(vertex_weights) == 1:
                edge_pos.append((cv, vertex_weights[0][1], budget if cv_count > 1 else budget//2, cv_count))
            else:
                edge_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
        final_possibilities = [(v[2] * v[3], v[2], v[0], v[1]) for v in edge_pos if v[2] > 0]
        final_possibilities.sort()
        # print(final_possibilities)
        if len(final_possibilities):
            # print("final", final_possibilities[-1])
            fin_choice = final_possibilities[-1][2], final_possibilities[-1][3], min(budget, final_possibilities[-1][1]) #take the edge that will maximize short run score
            # print("hero", fin_choice)
            return fin_choice #take the edge that will maximize short run score
        else:
            # calculate a score based on the expected winnings from each minimum vertex adjacent to a populated vertex
            # assert len(edge_pos) != 0
            min_list = [(x[0], min(list([(self.G[v[0]][v[1]]['weight'], v[1]) for v in self.edge_list if v[0] == x[1]]))[1]) for x in populated_vertices if x[1] not in self.ends]
            next_pos = []
            for cv_count, cv in min_list:
                if cv in self.ends:
                    continue
                vertex_weights = [(self.G[cv][v]['weight'], v) for v in list(self.G.neighbors(cv))]
                vertex_weights.sort()
                if len(vertex_weights) > 1:
                    next_pos.append((cv, vertex_weights[0][1], vertex_weights[1][0] - vertex_weights[0][0], cv_count))
            final_second = [(v[2] * v[3], v[2], v[0], v[1]) for v in next_pos if v[2] > 0]
            final_second.sort()
            # print("final_possibilities", final_possibilities)
            if len(final_second) == 0:
                # print("here")
                return self.begin, list(self.G.neighbors(self.begin))[0], 0 #skip this turn (very unlikely)

            #add as much as is reasonable to the second smallest edge

            # print("neighbors", list(self.G.neighbors(vertex)))
            fin_choice = final_second[-1][2], final_second[-1][3], min(budget, final_second[-1][1])
            # print("hero predicts", fin_choice)
            # print("helper move", fin_choice)
            # print(self.number_random)
            return fin_choice