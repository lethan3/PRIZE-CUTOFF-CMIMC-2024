import tkinter
import tkinter.filedialog
import pygame
import json
import math

"""
Visualizer instructions:
Press <- -> to go forward/back, hold for fast
Press C to toggle coordinate
Press Space to load another save
"""

# settings
COORD = False

# Constants for the hexagon grid
GRID_RADIUS = 4  # Number of paths most distant node
HEX_SIZE = 40  # Size of each hexagon
WIDTH, HEIGHT = 800, 600  # Window dimensions
BACKGROUND_COLOR = (0, 255, 255)  # Aqua
FPS = 30
players = ["white", "black", "red"]  # List of players

res = {}
step = 0
board = {}

node_coordinates = []
for x in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
    for y in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
        for z in range(-GRID_RADIUS + 1, GRID_RADIUS + 1):
            # Check if node is valid
            if 1 <= x + y + z <= 2:
                node_coordinates.append((x, y, z))


# Function to calculate the position of the nodes
def hex_to_pixel(x, y, z):
    xc = HEX_SIZE * (x / 2 + y / 2 - z)
    yc = -HEX_SIZE * (x * math.sqrt(3) / 2 - y * math.sqrt(3) / 2)
    return xc + WIDTH / 2, yc + HEIGHT / 2


def prompt_file():
    global res
    global step
    global board
    global players
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()

    with open(file_name, "r") as reader:
        res = json.load(reader)
    step = 0
    board = {}
    if res["game"][0][1]:
        board[tuple(res["game"][0][1])] = res["game"][0][0]
    players = res["name"]
    nstep = len(res["game"])
    print(f"Players: {players}")
    print(f"Total: {nstep} steps")
    return file_name


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

f = prompt_file()
pygame.display.set_caption(f)
running = True
Lcounter = 0
Rcounter = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                f = prompt_file()
            if event.key == pygame.K_c:
                COORD = 1 - COORD
            if event.key == pygame.K_LEFT:
                Lcounter = 0
            if event.key == pygame.K_RIGHT:
                Rcounter = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if step != 0:
                    if res["game"][step][1]:
                        del board[tuple(res["game"][step][1])]
                    step = step - 1
            if event.key == pygame.K_RIGHT:
                if step != len(res["game"]) - 1:
                    step = step + 1
                    if res["game"][step][1]:
                        board[tuple(res["game"][step][1])] = res["game"][step][0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        Lcounter += 1
    if keys[pygame.K_RIGHT]:
        Rcounter += 1
    if Lcounter > 10:
        if step != 0:
            if res["game"][step][1]:
                del board[tuple(res["game"][step][1])]
            step = step - 1

    if Rcounter > 10:
        if step != len(res["game"]) - 1:
            step = step + 1
            if res["game"][step][1]:
                board[tuple(res["game"][step][1])] = res["game"][step][0]
    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # print(node_coordinates)
    # Draw the nodes (vertices of hexagons)
    for x, y, z in node_coordinates:
        xc, yc = hex_to_pixel(x, y, z)
        pygame.draw.circle(screen, (0, 0, 0), (int(xc), int(yc)), 3)  # Black nodes

    # Draw the pieces
    for node, player in board.items():
        x, y, z = node
        xc, yc = hex_to_pixel(x, y, z)
        if player == 0:
            pygame.draw.circle(
                screen, (255, 255, 255), (int(xc), int(yc)), 15
            )  # White piece
        elif player == 1:
            pygame.draw.circle(screen, (0, 0, 0), (int(xc), int(yc)), 15)  # Black piece
        elif player == 2:
            pygame.draw.circle(screen, (255, 0, 0), (int(xc), int(yc)), 15)  # Red piece

    # Draw the longest path counters
    font = pygame.font.Font(None, 36)
    scores = res["game"][step][2]
    for idx, player in enumerate(players):
        text = font.render(f"{player.capitalize()}: {scores[idx]}", True, (0, 0, 0))
        screen.blit(text, (WIDTH - 300, 20 + idx * 40))

    # Coordinate?
    font = pygame.font.Font(None, 16)
    for x, y, z in node_coordinates:
        xc, yc = hex_to_pixel(x, y, z)
        if COORD:
            text = font.render(str((x, y, z)), True, "blue")
            screen.blit(text, (xc - 25, yc))

    pygame.display.flip()
    ## update title to show filename
    pygame.display.set_caption(f"- {step} - File: {f}")

    clock.tick(FPS)
pygame.quit()
