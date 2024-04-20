import json
import argparse
import math
import numpy as np

import time
import pygame

from utils import *

# Restrict dungeon to rooms (x,y) with max(x,y) <= RADIUS. Change to 1000 for some bonus problems
RADIUS = 100

# Restrict to MAX_STEP steps (days). Change to 1,000,000 for some bonus problems
MAX_STEP = 1000000

# Don't change this, this gives extra boundary for printing purposes
RADIUS += 1

# Resolution of pygame window
RESOLUTION = np.array([900, 900])


def getab(table, dungeon, alice, bob):
    ax = alice[0] + RADIUS
    ay = alice[1] + RADIUS
    bx = bob[0] + RADIUS
    by = bob[1] + RADIUS

    a = dungeon[ax, ay]
    b = dungeon[bx, by]

    return (a, b)


def step(table, dungeon, alice, bob):
    ax = alice[0] + RADIUS
    ay = alice[1] + RADIUS
    bx = bob[0] + RADIUS
    by = bob[1] + RADIUS

    a = dungeon[ax, ay]
    b = dungeon[bx, by]

    c, d, amove, bmove, _, _ = table[(a, b)]

    same = alice[0] == bob[0] and alice[1] == bob[1]
    if amove[0] == 0 and amove[1] == 0 and bmove[0] == 0 and bmove[1] == 0:
        if not same and a == c and b == d or same and a == c:
            # Halts
            return 1

    dungeon[bx, by] = d
    dungeon[ax, ay] = c  # Alice can overwrite Bob

    alice += amove
    bob += bmove

    if not inrange(alice, -RADIUS + 1, RADIUS - 1) or not inrange(
        bob, -RADIUS + 1, RADIUS - 1
    ):
        return -1

    return 0


def simulate(table, alphabet, dungeon, alice, bob, screen):
    def proj(x):
        return np.array(
            [
                (x[0] - VIEW_POS[0]) / VIEW_SIZE * RESOLUTION[0] / 2
                + RESOLUTION[0] / 2,
                (x[1] - VIEW_POS[1]) / VIEW_SIZE * RESOLUTION[0] / 2
                + RESOLUTION[0] / 2,
            ]
        )

    VIEW_POS = np.array([0.0, 0.0])
    VIEW_SIZE = 30
    SIM_RATE = 3
    MOUSE_DRAG = False
    MOUSE_POS = None

    steps = 0
    ticks = 0

    running = True  # Whether simulation is running
    ticking = False  # Whether program is running
    halts = False  # Whether program halted
    error = False  # Whether program raised error
    errormessage = "Terminated early"

    ab = getab(table, dungeon, alice, bob)
    if not ab in table:
        error = True
        errormessage = "Missing transition rule"

    while running:

        starttime = time.time()

        # Progress program by one day
        if not error and not halts:

            if ticks > 1000 / SIM_RATE:
                ticks = 0
                steps += 1

                outcode = step(table, dungeon, alice, bob)
                if outcode == 1:
                    halts = True
                elif outcode == -1:
                    error = True
                    errormessage = "Out of bounds"
                elif steps == MAX_STEP:
                    error = True
                    errormessage = "Exceeded max time steps"

            if not error:

                ab = getab(table, dungeon, alice, bob)
                if not ab in table:
                    error = True  # Missing transition rule
                    errormessage = "Missing transition rule"

        # handle input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                VIEW_SIZE *= math.exp(event.y / 10)
            elif event.type == pygame.KEYDOWN:

                key = event.key
                if key == pygame.K_UP:
                    if SIM_RATE < 50:
                        SIM_RATE *= 2
                elif key == pygame.K_DOWN:
                    if SIM_RATE > 0.2:
                        SIM_RATE *= 1 / 2
                elif key == pygame.K_RIGHT:
                    if not ticking:
                        ticks = 1000 / SIM_RATE + 1
                elif key == pygame.K_LEFT:
                    ticking = not ticking

                elif key == pygame.K_s:
                    np.save("dungeon.npy", dungeon)

                elif key == pygame.K_p:
                    print_dungeon(
                        steps,
                        alphabet,
                        dungeon,
                        alice + np.array([RADIUS, RADIUS]),
                        bob + np.array([RADIUS, RADIUS]),
                    )

                elif key == pygame.K_n:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                MOUSE_DRAG = True
                MOUSE_POS = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                MOUSE_DRAG = False
            elif MOUSE_DRAG and event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                diffx = mouse_position[0] - MOUSE_POS[0]
                diffy = mouse_position[1] - MOUSE_POS[1]
                VIEW_POS += np.array([-diffx, -diffy]) * 2 * VIEW_SIZE / RESOLUTION[0]
                MOUSE_POS = mouse_position

            elif event.type == pygame.QUIT:
                exit()

        # Draw visualization
        screen.fill((255, 255, 255))

        alice_cor = proj(alice + np.array([-0.5, -0.5]))
        alice_dim = proj(alice + np.array([0.5, 0.5])) - proj(
            alice + np.array([-0.5, -0.5])
        )
        bob_cor = proj(bob + np.array([-0.5, -0.5]))
        bob_dim = proj(bob + np.array([0.5, 0.5])) - proj(bob + np.array([-0.5, -0.5]))
        pygame.draw.rect(
            screen,
            (200, 255, 200),
            (alice_cor[0], alice_cor[1], alice_dim[0], alice_dim[1]),
        )
        pygame.draw.rect(
            screen, (200, 200, 255), (bob_cor[0], bob_cor[1], bob_dim[0], bob_dim[1])
        )

        left = max(int(VIEW_POS[0] - VIEW_SIZE) - 1, -RADIUS)
        right = min(int(VIEW_POS[0] + VIEW_SIZE) + 1, RADIUS)
        up = max(int(VIEW_POS[1] - VIEW_SIZE) - 1, -RADIUS)
        down = min(int(VIEW_POS[1] + VIEW_SIZE) + 1, RADIUS)

        font = pygame.font.Font(None, int(RESOLUTION[0] / VIEW_SIZE / 1.5))

        for i in range(left, right + 1):
            for j in range(up, down + 1):
                if dungeon[i + RADIUS, j + RADIUS] != 0:
                    text = font.render(
                        str(dungeon[i + RADIUS, j + RADIUS]), True, (0, 0, 0)
                    )
                    text_rec = text.get_rect(center=proj([i, j]))
                    screen.blit(text, text_rec)

        for i in range(left, right + 2):
            pygame.draw.aaline(
                screen,
                (230, 230, 230),
                proj([i - 0.5, up - 0.5]),
                proj([i - 0.5, down + 0.5]),
            )

        for j in range(up, down + 2):
            pygame.draw.aaline(
                screen,
                (230, 230, 230),
                proj([left - 0.5, j - 0.5]),
                proj([right + 0.5, j - 0.5]),
            )

        font = pygame.font.Font(None, 20)
        text = font.render(
            "Alice is green, Bob is blue. Move around with mouse drag and scroll.",
            True,
            (255, 0, 0),
        )
        screen.blit(text, (5, 5))
        text = font.render(
            "Print the dungeon as image with p key. Save the dungeon state (as .npy) with s key",
            True,
            (255, 0, 0),
        )
        screen.blit(text, (5, 25))
        text = font.render(
            "Pause/continue with left key, single step with right key. Switch to next test case with n key",
            True,
            (255, 0, 0),
        )
        screen.blit(text, (5, 45))

        text = font.render(
            "Change simulation rate with up/down keys. Simulation rate = "
            + str(SIM_RATE)
            + " steps per second",
            True,
            (255, 0, 0),
        )
        screen.blit(text, (5, 65))

        if error:
            text = font.render("Program raise error", True, (205, 0, 0))
            screen.blit(text, (5, 85))

            text = font.render(errormessage, True, (205, 0, 0))
            screen.blit(text, (5, 105))
        else:
            if halts:
                text = font.render("Program has halted", True, (205, 0, 0))
                screen.blit(text, (5, 85))
            elif ticking:
                text = font.render("Program running", True, (205, 0, 0))
                screen.blit(text, (5, 85))
            else:
                text = font.render("Program paused", True, (205, 0, 0))
                screen.blit(text, (5, 85))

            _, _, _, _, codetext, codecomment = table[getab(table, dungeon, alice, bob)]
            text = font.render("Transition rule = " + codetext, True, (205, 0, 0))
            screen.blit(text, (5, 105))
            if codecomment != None:
                text = font.render("Comment = " + codecomment, True, (205, 0, 0))
                screen.blit(text, (5, 125))

        pygame.display.flip()
        pasttime = (time.time() - starttime) * 1000
        if pasttime > 10:
            if ticking:
                ticks += pasttime
        else:
            pygame.time.wait(10 - int(pasttime))
            if ticking:
                ticks += 10

    return (dungeon, halts, steps, errormessage)


def main():
    parser = argparse.ArgumentParser(
        description="Dungeon journey visualizer CLI",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c", "--code", required=True, help="Path to code file to visualize"
    )
    parser.add_argument(
        "-t",
        "--test",
        required=False,
        help="Path to test file to visualize your code running on",
    )
    args = parser.parse_args()

    code = args.code
    trace = args.test

    with open(code) as file:
        lines = [line.rstrip() for line in file]

    table, alphabet = parse_code(lines)

    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)

    if trace != None:
        with open(trace) as file:
            tests = json.load(file)

        print("Your program has size " + str(len(alphabet)))
        for testcase in tests:

            inp = testcase["input"]

            dungeon = np.zeros((2 * RADIUS + 1, 2 * RADIUS + 1)).astype(int)
            alice = np.array([0, 0]).astype(int)
            bob = np.array([0, 0]).astype(int)

            for x, y, z in inp:
                dungeon[x + RADIUS, y + RADIUS] = z

            dungeon, halts, steps, errormessage = simulate(
                table, alphabet, dungeon, alice, bob, screen
            )

            if "output" in testcase:
                success = False
                otp = testcase["output"]
                if not halts:
                    print("Program failed. " + errormessage)
                else:
                    success = True
                    for x, y, z in otp:
                        if dungeon[x + RADIUS, y + RADIUS] != z:
                            success = False
                            print(
                                "Program failed. Incorrect output of "
                                + str(dungeon[x + RADIUS, y + RADIUS])
                                + " at ("
                                + str(x)
                                + ", "
                                + str(y)
                                + "). Correct output is "
                                + str(z)
                            )
                            break
                    if success:
                        print("Program suceeded")
            else:
                print("No intended output")

    else:
        dungeon = np.zeros((2 * RADIUS + 1, 2 * RADIUS + 1)).astype(int)
        alice = np.array([0, 0]).astype(int)
        bob = np.array([0, 0]).astype(int)

        dungeon, halts, steps, _ = simulate(
            table, alphabet, dungeon, alice, bob, screen
        )
        print("Ran for " + str(steps) + " steps")
        # print_dungeon(steps, alphabet, dungeon, alice + np.array([RADIUS,RADIUS]), bob + np.array([RADIUS,RADIUS]))


if __name__ == "__main__":
    main()
