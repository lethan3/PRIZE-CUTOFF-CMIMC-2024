import random

GRID_RADIUS = 3

def random_bot_move(board_copy, player):
    node_coordinates = []
    for x in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
        for y in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
            for z in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
                # Check if node is valid
                if 1 <= x + y + z <= 2:
                    node_coordinates.append((x, y, z))
    empty_nodes = [node for node in node_coordinates if node not in board_copy]
    if len(empty_nodes)==0:
        return None
    return random.choice(empty_nodes)