import json
import argparse
import math
import numpy as np

from utils import *

# Restrict dungeon to rooms (x,y) with max(x,y) <= RADIUS. Change to 1000 for some bonus problems
RADIUS = 100

# Restrict to MAX_STEP steps (days). Change to 1,000,000 for some bonus problems
MAX_STEP = 1000000

# Don't change this, this gives extra boundary for printing purposes
RADIUS += 1


def step(table, dungeon, alice, bob):
    """Perform one step of the simulation"""
    ax = alice[0] + RADIUS
    ay = alice[1] + RADIUS
    bx = bob[0] + RADIUS
    by = bob[1] + RADIUS

    a = dungeon[ax, ay]
    b = dungeon[bx, by]

    if not (a, b) in table:
        return -2

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


def simulate(table, dungeon, alice, bob):
    """Simulate the dungeon journey and return the final state of the dungeon, whether it halts, the number of steps, and an error message if applicable."""
    steps = 0
    halts = False
    error = False
    errormessage = ""

    while not error and not halts:

        steps += 1

        outcode = step(table, dungeon, alice, bob)
        if outcode == 1:
            halts = True
        elif outcode == -1:
            error = True
            errormessage = "Out of bounds"
        elif outcode == -2:
            error = True
            errormessage = "Missing transition rule"
        elif steps == MAX_STEP:
            error = True
            errormessage = "Exceeded max time steps"

    return (dungeon, halts, steps, errormessage)


def main():

    parser = argparse.ArgumentParser(
        description="Dungeon journey tester CLI",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-c", "--code", required=True, help="Path to code file to test")
    parser.add_argument(
        "-t", "--test", required=False, help="Path to test file to test your code on"
    )
    args = parser.parse_args()

    code = args.code
    trace = args.test

    with open(code) as file:
        lines = [line.rstrip() for line in file]

    table, alphabet = parse_code(lines)

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

            dungeon, halts, steps, errormessage = simulate(table, dungeon, alice, bob)

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

        dungeon, halts, steps, _ = simulate(table, dungeon, alice, bob)
        print("Ran for " + str(steps) + " steps")
        print_dungeon(
            steps,
            alphabet,
            dungeon,
            alice + np.array([RADIUS, RADIUS]),
            bob + np.array([RADIUS, RADIUS]),
        )


if __name__ == "__main__":
    main()
