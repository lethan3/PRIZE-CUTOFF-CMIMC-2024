import pygame
import math
import random
import time
import copy

# Constants for the hexagon grid
GRID_RADIUS = 4  # Number of paths most distant node
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
TABLE = {
    1: 0,
    2: 0,
    3: 1,
    4: 3,
    5: 0,
}  # table of scores for each size connect component


def get_coordinates():  # Generate a list of node coordinates (vertices of hexagons)
    node_coordinates = []
    # for x in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
    #    for y in range(max(-GRID_RADIUS, -x - GRID_RADIUS)+1, min(GRID_RADIUS, -x + GRID_RADIUS) + 1):
    #        for z in range(max(-GRID_RADIUS, -x - y - GRID_RADIUS)+1, min(GRID_RADIUS, -x - y + GRID_RADIUS) + 1):
    for x in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
        for y in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
            for z in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
                # Check if node is valid
                if 1 <= x + y + z <= 2:
                    node_coordinates.append((x, y, z))
    return node_coordinates


def get_diameter(board, start_node, visit):  # Get longest path in a connected component
    def neighbors(node):
        # return SELECT_VALID(ALL_NEIGHBOR(*(node)))
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
    except Exception as exc:
        print("node empty?")
        print(exc)
        return 0

    connected = dict()
    con(start_node)
    # print(connected)
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


def score(board):  # return current score for each player

    visit = {pos: 0 for pos in node_coordinates}
    scores = [0, 0, 0]
    for pos in board.keys():
        if not visit[pos]:
            d = get_diameter(board, pos, visit)
            if d:
                scores[board[pos]] += TABLE[d]
    return scores


node_coordinates = get_coordinates()
NEIGHBOR_LIST = dict(
    zip(
        node_coordinates,
        [SELECT_VALID(ALL_NEIGHBOR(*(node))) for node in node_coordinates],
    )
)


def run_game(bot_list):
    player_list = list(bot_list.keys())
    funcs = list(bot_list.values())

    # Initialize the game state
    free_coordinates = node_coordinates.copy()
    board = {}  # Dictionary to track the state of the board
    players = ["white", "black", "red"]  # List of players
    players2id = {"white": 0, "black": 1, "red": 2}  # Players to ID
    current_player_idx = 0  # Index to keep track of the current player
    res = {"name": player_list, "scores": None, "game": []}  # For recording the results

    running = True

    ### implement early ending when all players choose not to move

    stop_count = 0

    while running:
        if (
            stop_count >= 3 or len(free_coordinates) == 0
        ):  # game ends without valid move
            scores = score(board)
            res["scores"] = scores
            break
        board_copy = copy.deepcopy(board)
        curfunc = funcs[current_player_idx]
        bot_move = curfunc(board_copy, current_player_idx)
        if (
            bot_move and isinstance(bot_move, tuple) and bot_move in free_coordinates
        ):  # If valid move
            # print(f"bot {current_player_idx} moves at {bot_move}")
            board[bot_move] = current_player_idx
            free_coordinates.remove(bot_move)
            scores = score(board)
            res["game"].append([current_player_idx, bot_move, scores])
            stop_count = 0
        else:  # If not valid move, pass
            # print(f"{players[current_player_idx]} is not making a valid move!")
            scores = score(board)
            res["game"].append([current_player_idx, None, scores])
            stop_count += 1

        current_player_idx = (current_player_idx + 1) % len(players)

    return res
