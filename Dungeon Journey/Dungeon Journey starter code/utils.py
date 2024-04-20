import re
import numpy as np
import matplotlib
from PIL import Image


def inrange(L, lower, upper):
    return all(map(lambda q: lower <= q and q <= upper, L))


def parse_code(lines):
    directions = {
        "U": np.array([0, -1]),
        "D": np.array([0, 1]),
        "L": np.array([-1, 0]),
        "R": np.array([1, 0]),
        "_": np.array([0, 0]),
    }
    table = {}

    for i in range(len(lines)):
        if lines[i] == "" or lines[i] == "\n" or lines[i][0] == "%":
            continue

        line = lines[i].split("%", 1)
        code = re.findall(r"[^,\s]+", line[0])
        if len(code) != 6:
            print(
                "Error on line "
                + str(i)
                + ": Incorrect number of values (there should be six)"
            )
            print(lines[i])
            exit()

        comment = None
        if len(line) > 1:
            comment = line[1]

        a, b, c, d = code[0:4]
        a = int(a)
        b = int(b)
        c = a if c == "_" else int(c)
        d = b if d == "_" else int(d)

        if (a, b) in table:
            print("Error on line " + str(i) + ": Input has already appeared before")
            print(lines[i])
            exit()
        assert not (a, b) in table
        if not inrange([a, b, c, d], 0, 99):
            print(
                "Error on line "
                + str(i)
                + ": Input and output numbers should be between 0 and 99"
            )
            print(lines[i])
            exit()
        if not (code[4] in directions and code[5] in directions):
            print("Error on line " + str(i) + ": Invalid direction")
            print(lines[i])
            exit()

        table[(a, b)] = [
            c,
            d,
            directions[code[4]],
            directions[code[5]],
            line[0],
            comment,
        ]

    alph = set()
    for a, b in table.keys():
        alph.add(a)
        alph.add(b)
    alphabet = list(alph)
    alphabet.sort()

    return table, alphabet


def print_dungeon(steps, alphabet, dungeon, alice, bob):
    path = "dungeon at " + str(steps) + " steps.png"
    dungeon = np.transpose(dungeon)

    assert len(alphabet) >= 2
    cm = matplotlib.colormaps["viridis"].colors

    def query(c, channel):
        if c == 0:
            return 255
        idx = alphabet.index(c)  # Your code should cover all colors in input
        color = cm[(255 * idx) // (len(alphabet) - 1)][channel] * 255
        return color

    dp0 = np.vectorize(lambda c: query(c, 0))(dungeon)
    dp1 = np.vectorize(lambda c: query(c, 1))(dungeon)
    dp2 = np.vectorize(lambda c: query(c, 2))(dungeon)
    dp = (np.stack([dp0, dp1, dp2], axis=-1)).astype(np.uint8)

    # For small dungeons upsample and mark Alice, Bob
    if dp.shape[1] < 250:
        dp = np.repeat(dp, 4, axis=0)
        dp = np.repeat(dp, 4, axis=1)

        mask = [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]]
        for i in range(4):
            for j in range(4):
                if mask[i][j] == 1:
                    dp[4 * alice[1] + i, 4 * alice[0] + j, :] = np.array([255, 0, 0])
                    dp[4 * bob[1] + i, 4 * bob[0] + j, :] = np.array([255, 0, 0])

    # For large dungeons just mark Alice Bob
    else:
        dp[alice[1], alice[0], :] = np.array([255, 0, 0])
        dp[bob[1], bob[0], :] = np.array([255, 0, 0])

    im = Image.fromarray(dp)
    im.save(path)
