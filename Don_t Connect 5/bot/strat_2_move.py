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

# FIND ALL DIAMETER 4 CCs

all_diam_4 = set()

curr_cc_4 = []
def dfs4(node, depth = 1):
    curr_cc_4.append(node)

    if (depth == 4):
        if curr_cc_4[-1] > curr_cc_4[0]:
            all_diam_4.add(tuple(curr_cc_4))
        curr_cc_4.pop(-1)
        return

    for ne in NEIGHBOR_LIST[node]:
        if ne not in curr_cc_4:
            dfs4(ne, depth + 1)
    
    curr_cc_4.pop(-1)

for node in node_coordinates:
    dfs4(node)

# print(len(all_diam_4))

new_diam_4 = set()

for cc in all_diam_4:
    cc = list(cc)
    for i in range(2):
        for j in range(2):
            ncc = cc
            if i:
                for ne in NEIGHBOR_LIST[ncc[1]]:
                    if ne not in ncc:
                        ncc.append(ne)
            if j:
                for ne in NEIGHBOR_LIST[ncc[2]]:
                    if ne not in ncc:
                        ncc.append(ne)
            
            new_diam_4.add(tuple(ncc))

all_diam_4 |= new_diam_4

# print(len(all_diam_4))

find_cc4_by_node = {}

for cc in all_diam_4:
    for i in range(len(cc)):
        if cc[i] in find_cc4_by_node:
            find_cc4_by_node[cc[i]].append(cc)
        else:
            find_cc4_by_node[cc[i]] = [cc]

# FIND ALL DIAMETER 3 CCs


all_diam_3 = set()

curr_cc_3 = []
def dfs3(node, depth = 1):
    curr_cc_3.append(node)

    if (depth == 4):
        if curr_cc_3[-1] > curr_cc_3[0]:
            all_diam_3.add(tuple(curr_cc_3))
        curr_cc_3.pop(-1)
        return

    for ne in NEIGHBOR_LIST[node]:
        if ne not in curr_cc_3:
            dfs3(ne, depth + 1)
    
    curr_cc_3.pop(-1)

for node in node_coordinates:
    dfs3(node)

# print(len(all_diam_3))

new_diam_3 = set()

for cc in all_diam_3:
    cc = list(cc)
    for i in range(2):
        ncc = cc
        if i:
            for ne in NEIGHBOR_LIST[ncc[1]]:
                if ne not in ncc:
                    ncc.append(ne)
        new_diam_3.add(tuple(ncc))

all_diam_3 |= new_diam_3

# print(len(all_diam_3))

find_cc3_by_node = {}

for cc in all_diam_3:
    for i in range(len(cc)):
        if cc[i] in find_cc3_by_node:
            find_cc3_by_node[cc[i]].append(cc)
        else:
            find_cc3_by_node[cc[i]] = [cc]
            

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

    # print(start_node, "len(connected)", len(connected))
    #print(connected)
    if len(connected) <= 3: # must be a line
        return len(connected)
    if 4 <= len(connected) <= 5: # a star if we have a deg-3 node, a line otherwise
        if 3 in connected.values(): # It's a star!
            return len(connected) - 1
        return len(connected)
    if 6 == len(connected):
        three = list(connected.values())
        if 3 in connected.values():
            three.remove(3)
            if 3 in three:
                return 4 # this is a shape x - x - x - x
                        #                     x   x
        return 5 # diameter is 5 otherwise

    # For the larger(>6) ones, diameter must be larger than 5 so we just return 5
    return 5
    # maxl = 0

    # for node in connected:
    #     maxl = max(maxl, dfs(node))
    # return maxl

def score(board): # return current score for each player
    visit = {pos:0 for pos in node_coordinates}
    scores = {0:0 , 1:0, 2:0}
    for pos in board.keys():
        if not visit[pos]:
            d = get_diameter(board, pos, visit)
            if d:
                scores[board[pos]] += TABLE[d]
    return scores

move_num = -1
smove = [62]

def find_working_cc(board_copy, node, find_set):
    q = deque()
    q.append((node, 0))

    enemy_cc = set()
    enemy_cc.add(node)

    liberties = []
    while not len(q) == 0:
        qnode, d = q[0]
        q.popleft()
        for ne in NEIGHBOR_LIST[qnode]:
            if ne not in enemy_cc and ne in board_copy and board_copy[ne] == board_copy[qnode]:
                q.append((ne, d + 1))
                enemy_cc.add(ne)
            if ne not in board_copy:
                liberties.append(ne)
    
    working_cc4 = []

    for cc4 in find_set[node]:
        if move_num in smove: print(cc4)
        # check that enemy_cc is subset of cc4
        is_subset = True
        for a in enemy_cc:
            if a not in cc4:
                if move_num in smove: print(a)
                is_subset = False
                break

        if not is_subset:
            if move_num in smove: print('not subset')
            continue

        addl = 0
        for a in cc4:
            if a not in board_copy:
                addl += 1
        

        # check that no neighbors
        no_neighbors = True
        for cc4_node in cc4:
            for cc4_ne in NEIGHBOR_LIST[cc4_node]:
                if (cc4_ne in cc4 or cc4_ne in enemy_cc): continue
                if cc4_ne in board_copy and board_copy[cc4_ne] == board_copy[node]:
                    no_neighbors = False
                    break

        if not no_neighbors:
            if move_num in smove: print('has neighbors')
            continue

        # check that all in cc4 is safe and untaken
        all_safe = True
        for cc4_node in cc4:
            if cc4_node in board_copy:
                if board_copy[cc4_node] != board_copy[node]:
                    if move_num in smove: print('taken')
                    all_safe = False
                    break
            if cc4_node not in board_copy and see_move(board_copy, board_copy[node], cc4_node) == -1:
                if move_num in smove: print('unsafe')
                all_safe = False
                break
        
        if not all_safe:
            continue
        
        # cc4 is valid

        if move_num in smove: print('appended')
        working_cc4.append((addl, cc4))
    
    working_cc4.sort()

    return (enemy_cc, liberties, working_cc4)

def find_sabotage(board_copy, player):
    global first_move
    found = [set(), set(), set()]

    visit_cc = {p:0 for p in node_coordinates}
    visited = set()

    for node in board_copy:
        if (board_copy[node] == player or node in visited): continue

        if move_num in smove:
            print("NODE:", node)

        enemy_cc, liberties, working_cc4 = find_working_cc(board_copy, node, find_cc4_by_node)

        if get_diameter(board_copy, node, visit_cc) >= 4 or len(enemy_cc) <= 1:
            # group already has diam 4
            if move_num in smove:
                print("skipped")
            continue

        if len(working_cc4) == 0:
            # group is dead
            continue

        if move_num in smove: print('number of working cc4:', len(working_cc4))

        for lib in liberties:
            cc4_not_in = []
            for cc_a in working_cc4:
                if lib not in cc_a[1]:
                    cc4_not_in.append(cc_a)
        
            cc4_not_in.sort(key=lambda a : len(a))
        
            if len(working_cc4) and len(cc4_not_in) == 0:
                if working_cc4[0][0] < 2 and len(working_cc4) >= 2:
                    if move_num in smove: print("found sabotage, complete block:", lib)
                    found[board_copy[node]].add(lib)
                else:
                    if move_num in smove: print("no complete block, 2 moves to fill:", lib)
            elif len(working_cc4) and len(cc4_not_in) and working_cc4[0][0] < cc4_not_in[0][0]:
                if working_cc4[0][0] < 2 and len(working_cc4) >= 2:
                    if move_num in smove: print("found sabotage, limit block:", lib)
                    found[board_copy[node]].add(lib)
                else:
                    if move_num in smove: print("no limit block, 2 moves to fill:", lib)


    return found

def see_move(board_copy, player, pos): # see if move ruins, builds 4, builds 3, builds 2, or none
    neighbor_diameters = []
    for ne in NEIGHBOR_LIST[pos]:
        if (ne in board_copy and board_copy[ne] == player):
            visit = {p:0 for p in node_coordinates}
            neighbor_diameters.append(get_diameter(board_copy, ne, visit))

    board_new = board_copy.copy()
    board_new[pos] = player

    visit = {p:0 for p in node_coordinates}
    
    # print("QUERYING", pos)
    new_diameter = get_diameter(board_new, pos, visit)
    # print(" diameter: ", pos, new_diameter)
    
    if (new_diameter >= 5): return -1
    if (new_diameter == 4 and max(neighbor_diameters) < 4): return 4 
    if (new_diameter == 3 and max(neighbor_diameters) < 3): return 3
    if (new_diameter == 2 and max(neighbor_diameters) < 2): return 2
    if (new_diameter == 1): return 1

    return 0.5

def on_border(pos):
    return min(pos) == -GRID_RADIUS + 1 or max(pos) == GRID_RADIUS

def on_inborder(pos):
    if (min(pos) == -GRID_RADIUS + 1) and (max(pos) == GRID_RADIUS):
        return False
    if (min(pos) == -GRID_RADIUS + 1):
        return sum(pos) % 2
    if (max(pos) == GRID_RADIUS):
        return not (sum(pos) % 2)
    return False

def on_outborder(pos):
    return on_border(pos) and not on_inborder(pos)

turn = 0

def openness_value(board_copy, player, pos): # return how open a cell is for expansion
    board_new = board_copy.copy()
    board_new[pos] = player

    if see_move(board_copy, (player + 1) % 3, pos) == -1 and see_move(board_copy, (player + 2) % 3, pos) == -1:
        return 0
    
    player_cc, liberties, working_cc4 = find_working_cc(board_new, pos, find_cc4_by_node)

    player_cc, liberties, working_cc3 = find_working_cc(board_new, pos, find_cc3_by_node)

    if len(working_cc3) == 0:
        return 0
    
    open_val = 0

    if on_inborder(pos):
        open_val += 1
    if on_outborder(pos):
        open_val -= 2

    for i in range(3):
        for j in range(3):
            if (i == j): continue
            dist_2 = [pos[0], pos[1], pos[2]]
            dist_2[i] += 1
            dist_2[j] -= 1
            dist_2 = tuple(dist_2)
            
            if (dist_2 in board_copy and board_copy[dist_2] == player):
                # dist_2_good = True
                open_val += 3

    # if (dist_2_good):
    #     open_val += 3
    
    return 10000 * min(len(working_cc4), turn // 4 + 1) + 100 * min(len(working_cc3), turn // 4 + 1) + open_val

    # if diam < 3:
    #     return 0

    # if diam == 3:
    #     return open_val

    # return open_val + 100

def top_move(board_copy, player):
    # if have a complete, take that
    # if have a sabotage, take that
    # else, take max(see_move, openness_value)

    fs = find_sabotage(board_copy, player)
    sc = score(board_copy)
    
    enes = [0, 1, 2]
    enes.pop(player)
    if (sc[enes[0]] > sc[enes[1]]): 
        enes[0], enes[1] = enes[1], enes[0]
    
    moves = []
    for node in node_coordinates:
        if node not in board_copy:
            val = see_move(board_copy, player, node)
            sab_val = 2 if node in fs[enes[1]] else 1 if node in fs[enes[0]] else 0
            ov = openness_value(board_copy, player, node)

            moves.append((val, sab_val, ov, node))

    moves.append((0, 0, 0, None))
    moves.sort(reverse=True)

    if move_num in smove: print(moves)
    if move_num in smove: print("+++++++++++++++")

    for move in moves:
        if (move[0] == 4) and move[2] < 20000:
            return move
    
    for move in moves:
        if (move[1] and move[0] != -1):
            return move
    
    for move in moves:
        if (move[0] == 4):
            return move

    # print(moves[0][0], ':', moves[0][3])
    for move in moves:
        if move[2] != 0 and move[0] != -1:
            return move
    
    return moves[0]

def strat_2_move(board_copy, player):
    global move_num, turn
    move_num += 3

    turn = 1
    for b in board_copy:
        if board_copy[b] == player:
            turn += 1

    sc = score(board_copy)
    enes = [0, 1, 2]
    enes.pop(player)
    if (sc[enes[0]] > sc[enes[1]]): 
        enes[0], enes[1] = enes[1], enes[0]

    ene_moves = [top_move(board_copy, enes[0]), top_move(board_copy, enes[1])]
    my_move = top_move(board_copy, player)

    if ((my_move[2] == 0 or my_move[0] < 1) and my_move[1] == 0):
        # move won't be able to form diameter 3 or sabotage

        poss_moves = []

        if ene_moves[1][3] is not None and see_move(board_copy, player, ene_moves[1][3]) != -1:
            poss_moves.append(ene_moves[1])
            if ene_moves[1][0] >= 3:
                return ene_moves[1][3]
        if ene_moves[0][3] is not None and see_move(board_copy, player, ene_moves[0][3]) != -1:
            poss_moves.append(ene_moves[0])
            if ene_moves[0][0] >= 3:
                return ene_moves[0][3]
        
        # poss_moves.sort(reverse=True)
        if len(poss_moves):
            # print('no good move, block', poss_moves[0])
            return poss_moves[0][3]
        else:
            # print('no good move, no block', my_move)
            # if my_move[1]: print(move_num, "SABOTAGE")
            return my_move[3]
    
    # print('good move', my_move)
    # if my_move[1]: print(move_num, "SABOTAGE")
    # print(turn, my_move)
    return my_move[3]
