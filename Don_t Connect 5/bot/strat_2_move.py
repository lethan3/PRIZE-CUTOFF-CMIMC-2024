import random
from collections import deque

GRID_RADIUS = 4
node_coordinates = []
ALL_NEIGHBOR = lambda x, y, z: ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)) # make this more efficient?
SELECT_VALID = lambda lis: [(x, y, z) for (x, y, z) in lis if 1 <= x + y + z <= 2 and -GRID_RADIUS + 1 <= x <= GRID_RADIUS and -GRID_RADIUS + 1 <= y <= GRID_RADIUS and -GRID_RADIUS + 1 <= z <= GRID_RADIUS] # keep those within-bound
TABLE = {1:0, 2:0, 3:1, 4:3, 5:0}


for x in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
    for y in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
        for z in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
            # Check if node is valid
            if 1 <= x + y + z <= 2:
                node_coordinates.append((x, y, z))

NEIGHBOR_LIST = dict(zip(node_coordinates, [SELECT_VALID(ALL_NEIGHBOR(*(node))) for node in node_coordinates]))

def get_diameter(board, start_node, visit): 
    def neighbors(node):
        #return SELECT_VALID(ALL_NEIGHBOR(*(node)))
        return NEIGHBOR_LIST[node]
    def con(node): # Find connected component and respective degrees
        visit[node] = 1
        connected[node] = -1
        cnt = 0
        for neighbor in neighbors(node):
            if neighbor in board and board[neighbor] == player:
                cnt += 1
                if neighbor not in connected:
                    con(neighbor)
        connected[node] = cnt
    def dfs(node, visited = set()):
        visited.add(node)
        max_path_length = 0
        for neighbor in neighbors(node):
            if neighbor in board and board[neighbor] == player and neighbor not in visited:
                path_length = dfs(neighbor, visited.copy())
                max_path_length = max(max_path_length, path_length)
        return max_path_length + 1
    
    try:
        player = board[start_node]
    except Exception as exc:
        print("node empty?")
        print(exc)
        return 0

    connected = dict()
    con(start_node)
    #print(connected)
    ret = 0

    if len(connected) <= 3: # must be a line
        ret = len(connected)
    elif 4 <= len(connected) <= 5: # a star if we have a deg-3 node, a line otherwise
        if 3 in connected.values(): # It's a star!
            ret = len(connected) - 1
        else:
            ret = len(connected)
    elif 6 == len(connected):
        three = list(connected.values())
        if 3 in connected.values():
            three.remove(3)
            if 3 in connected.values():
                ret = 4 # this is a shape x - x - x - x
                        #                     x   x
            else: ret = 5 # diameter is 5 otherwise
        else:
            ret = 5
    # For the larger(>6) ones, diameter must be larger than 5 so we just return 5
    else:
        ret = 5
    # maxl = 0

    # for node in connected:
    #     maxl = max(maxl, dfs(node))
    # return maxl

    return ret

def score(board): # return current score for each player
    visit = {pos:0 for pos in node_coordinates}
    scores = {0:0 , 1:0, 2:0}
    for pos in board.keys():
        if not visit[pos]:
            d = get_diameter(board, pos, visit)
            if d:
                scores[board[pos]] += TABLE[d]
    return scores

def find_sabotage(board_copy, player):
    found = [None, None, None]

    visit_cc = {p:0 for p in node_coordinates}
    visited = set()

    for node in board_copy:
        if (board_copy[node] == player or node in visited): continue

        q = deque()
        q.append((node, 0))
        visited.add(node)

        liberty = None
        liberties = 0
        while not len(q) == 0:
            node, d = q[0]
            q.popleft()
            for ne in NEIGHBOR_LIST[node]:
                if ne not in visited and ne in board_copy and board_copy[ne] == board_copy[node]:
                    q.append((ne, d + 1))
                    visited.add(ne)
                if ne not in board_copy:
                    liberties += 1
                    liberty = ne

        if (liberties == 1):
            curr_diameter = get_diameter(board_copy, node, visit_cc)
            board_new = board_copy.copy()
            board_new[liberty] = board_copy[node]

            visit = {p:0 for p in node_coordinates}
            new_diameter = get_diameter(board_new, liberty, visit)
            
            if (curr_diameter < 4 and new_diameter == 4):
                found[board_copy[node]] = liberty

    return found



def see_move(board_copy, player, pos): # see if move ruins, builds 4, builds 3, builds 2, or none
    neighbor_diameters = []
    for ne in NEIGHBOR_LIST[pos]:
        if (ne in board_copy and board_copy[ne] == player):
            visit = {pos:0 for pos in node_coordinates}
            neighbor_diameters.append(get_diameter(board_copy, ne, visit))

    board_new = board_copy.copy()
    board_new[pos] = player

    visit = {p:0 for p in node_coordinates}
    new_diameter = get_diameter(board_new, pos, visit)
    
    if (new_diameter >= 5): return -1
    if (new_diameter == 4 and max(neighbor_diameters) < 4): return 4 
    if (new_diameter == 3 and max(neighbor_diameters) < 3): return 3
    if (new_diameter == 2 and max(neighbor_diameters) < 2): return 2
    return 1

def openness_value(board_copy, player, pos): # return how open a cell is for expansion
    q = deque()
    q.append((pos, 0))

    visited = set(pos)

    open_val = 0
    while not len(q) == 0:
        node, d = q[0]
        q.popleft()
        if (d != 0): open_val += 1 / d
        for ne in NEIGHBOR_LIST[node]:
            if ne not in visited and ne not in board_copy:
                q.append((ne, d + 1))
                visited.add(ne)
    
    return open_val



def strat_2_move(board_copy, player):
    # if have a move, take that
    # if have a sabotage, take that
    # else, take max(see_move, openness_value)

    for node in node_coordinates:
        if node not in board_copy:
            val = see_move(board_copy, player, node)
            if (val == 4):
                return node
    
    fs = find_sabotage(board_copy, player)
    sc = score(board_copy)

    sab_move = None
    for i in range(3):
        if (i == player): continue
        if (sc[i] == max(sc)):
            sab_move = fs[i] if fs[i] is not None else sab_move
        else:
            sab_move = fs[i] if sab_move is None else sab_move

    if sab_move is not None:
        return sab_move
    
    moves = []
    for node in node_coordinates:
        if node not in board_copy:
            val = see_move(board_copy, player, node)
            ov = openness_value(board_copy, player, node)
            moves.append((val, ov, node))

    moves.append((0, 0, None))
    moves.sort()
    # print(moves[-1][2])
    return moves[-1][2]
    
