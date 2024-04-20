GRID_RADIUS = 4
ALL_NEIGHBOR = lambda x, y, z: (
    (x + 1, y, z),
    (x - 1, y, z),
    (x, y + 1, z),
    (x, y - 1, z),
    (x, y, z + 1),
    (x, y, z - 1),
)  # make this more efficient?
SELECT_VALID = lambda lis: [
    (x, y, z)
    for (x, y, z) in lis
    if 1 <= x + y + z <= 2
    and -GRID_RADIUS + 1 <= x <= GRID_RADIUS
    and -GRID_RADIUS + 1 <= y <= GRID_RADIUS
    and -GRID_RADIUS + 1 <= z <= GRID_RADIUS
]  # keep those within-bound
TABLE = {1: 0, 2: 0, 3: 1, 4: 3, 5: 0}


def get_coordinates():
    """
    Generate a list of node coordinates (vertices of hexagons)
    """
    node_coordinates = []
    for x in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
        for y in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
            for z in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
                # Check if node is valid
                if 1 <= x + y + z <= 2:
                    node_coordinates.append((x, y, z))
    return node_coordinates


def get_neighbor(node_coordinates):
    """
    Return a dict of list of coordinates for the neighbor(s) of each node in node_coordinates
    """
    return dict(
        zip(
            node_coordinates,
            [SELECT_VALID(ALL_NEIGHBOR(*(node))) for node in node_coordinates],
        )
    )


node_coordinates = get_coordinates()
NEIGHBOR_LIST = get_neighbor(node_coordinates)


def get_diameter(board, start_node, visit):
    """
    get the diameter of a connected component starting from start_node and update a visit dictionary(see `score` function)
    """

    def neighbors(node):
        return NEIGHBOR_LIST[node]

    def con(node):  # Find connected component and respective degrees
        visit[node] = 1
        connected[node] = -1
        cnt = 0
        for neighbor in neighbors(node):
            if neighbor in board and board[neighbor] == player:
                cnt += 1
                if neighbor not in connected:
                    con(neighbor)
        connected[node] = cnt

    def dfs(node, visited=set()):
        visited.add(node)
        max_path_length = 0
        for neighbor in neighbors(node):
            if (
                neighbor in board
                and board[neighbor] == player
                and neighbor not in visited
            ):
                path_length = dfs(neighbor, visited.copy())
                max_path_length = max(max_path_length, path_length)
        return max_path_length + 1

    try:
        player = board[start_node]
    except:
        return 0  # start node not occupied

    connected = dict()
    con(start_node)
    if len(connected) <= 3:  # must be a line
        return len(connected)
    if 4 <= len(connected) <= 5:  # a star if we have a deg-3 node, a line otherwise
        if 3 in connected.values():  # It's a star!
            return len(connected) - 1
        return len(connected)
    if 6 == len(connected):
        three = list(connected.values())
        if 3 in connected.values():
            three.remove(3)
            if 3 in three:
                return 4  # this is a shape x - x - x - x
                #                     x   x
        return 5  # diameter is 5 otherwise
    # For the larger(>6) ones, diameter must be larger than 5 so we just return 5
    return 5


def score(board):
    """
    return score for each player in some board configuration
    """
    visit = {pos: 0 for pos in node_coordinates}
    scores = {0: 0, 1: 0, 2: 0}
    for pos in board.keys():
        if not visit[pos]:
            d = get_diameter(board, pos, visit)
            if d:
                scores[board[pos]] += TABLE[d]
    return scores
