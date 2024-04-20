import random

GRID_RADIUS = 3
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

diameters = {}

def get_diameter(board, start_node, visit, upd_diameters = False): 
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

    for node in connected:
        diameters[node] = ret
    
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

def eval_move(board_copy, player, pos): # return the value of a move played by player
    # see what diameter cc this move would create
    neighbor_diameters = []
    for ne in NEIGHBOR_LIST[pos]:
        if (ne in board_copy and board_copy[ne] == player):
            visit = {pos:0 for pos in node_coordinates}
            neighbor_diameters.append(get_diameter(board_copy, ne, visit))

    board_new = board_copy.copy()
    board_new[pos] = player

    ferr = open('debug.txt', 'a')
    if (len(board_new) < 16): print(board_new, file=ferr)
    visit = {p:0 for p in node_coordinates}
    new_diameter = get_diameter(board_new, pos, visit)
    print(new_diameter, neighbor_diameters, file=ferr)

    ferr.close()


    if (new_diameter == 5): return -1
    if (new_diameter == 4 and max(neighbor_diameters) < 4 and sum(neighbor_diameters) != 9): return len(board_copy) // 3 - 5
    if (new_diameter == 3 and max(neighbor_diameters) < 3): return 2
    if (new_diameter >= 4 and 4 in neighbor_diameters): return -1

    # determine dist 2 score

    val = 0
    for i in range(3):
        for j in range(3):
            if (i == j): continue
            step_pos = [pos[0], pos[1], pos[2]] # dist 1
            if (sum(pos) == 1):
                step_pos[i] += 1
            else:
                step_pos[j] -= 1
            
            jump_pos = [pos[0], pos[1], pos[2]] # dist 2
            jump_pos[i] += 1
            jump_pos[j] -= 1

            step_pos, jump_pos = tuple(step_pos), tuple(jump_pos)

            if (step_pos not in board_copy and jump_pos in board_copy and board_copy[jump_pos] == player):
                if (diameters[jump_pos] >= 3): 
                    # print('bad')
                    val -= 1
                else: 
                    # print('good')
                    val += 1
    
    return val


    

def strat_1_move(board_copy, player):
    diameters.clear()

    visit = {p:0 for p in node_coordinates}
    for node in board_copy:
        if not visit[node] and node in board_copy:
            get_diameter(board_copy, node, visit, True)

    print('Diameters:', diameters, '\n', file=open('debug.txt', 'a'))


    maxscore = 0
    moves = []

    max_val = -1e9
    for node in node_coordinates:
        if node not in board_copy:
            val = eval_move(board_copy, player, node)

            print("VAL:", val, file=open('debug.txt', 'a'))
            if (val < max_val): continue
            elif (val == max_val):
                moves.append(node)
            else:
                moves.clear()
                moves.append(node)
                max_val = val


    print('FINAL:', max_val, '\n', file=open('debug.txt', 'a'))
    #print(maxscore)
    #print(select)
    if len(moves)==0:
        return None
    return random.choice(moves)