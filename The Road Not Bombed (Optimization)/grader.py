import random
from strategy import Planner

"""
Modify the parameters below for different tasks
"""

# Task 1: p = 5, bd = 0.25
p = 5  # number of cities
bd = 0.25  # bomb density

# Task 2: p = 5, bd = 0.1
# p = 5 # number of cities
# bd = 0.1 # bomb density

# Task 3: p = 1, bd = 0.25
# p = 1 # number of cities
# bd = 0.25 # bomb density

# Task 4: p = 1, bd = 0.1
# p = 1 # number of cities
# bd = 0.1 # bomb density

rng_grader = random.Random()  # use this for generating fixed setup
rng_grader.seed(19260817)

VERBOSE = True  # print more details
LAST = True  # whether to print the last query made in each TC
n = 16  # board size is n*n
q = 100  # number of queries


def runGrader(soln, pairs, bombs):
    # pairs represented as array of length p, each element is a length 2 array of length 2 array of coordinates
    # bombs represented with n*m array, '1' denotes bomb, '0' denotes no bomb
    print("Running")
    soln.setup(pairs, bd)

    queryOutputList = []
    bestScore = n * n + 1
    qloc = q
    while qloc > 0:
        roadplan = soln.query(qloc, queryOutputList)
        output, score = analyzeRoadPlan(roadplan, pairs, bombs)
        queryOutputList.append(output)

        qloc -= 1

        if score < bestScore:
            bestScore = score
            if VERBOSE:  # Draw state whenever a better score is achieved
                drawState(n, qloc, bombs, pairs, roadplan, score, queryOutputList)
    if qloc == 0 and LAST:
        drawState(n, qloc, bombs, pairs, roadplan, score, queryOutputList)
    print(f"Best score: {bestScore}")
    return bestScore


def drawState(n, q, bombs, pairs, plan, score, queryList):
    mapp = [[" "] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            if bombs[i][j] == 1:
                if plan[i][j] == 0:
                    mapp[i][j] = "."  # Missed Bomb
                else:
                    mapp[i][j] = "-"  # Bomb Hits Road
            else:
                if plan[i][j] == 0:
                    mapp[i][j] = " "  # Empty
                else:
                    mapp[i][j] = "#"  # Surivivng Road

    for i in range(len(pairs)):
        mapp[pairs[i][0][0]][pairs[i][0][1]] = i
        mapp[pairs[i][1][0]][pairs[i][1][1]] = i

    print("-" * (n + 2))
    for row in range(n):
        string = ""
        for col in range(n):
            string += " " + str(mapp[row][col]) + ""
        print("|" + string + "|")
    print("-" * (n + 2))
    print(str(q) + " queries remaining")
    print("Score: " + str(score))
    print("Query History: " + str(queryList))


def generateSetup(n, p, bd):
    bombs = [[0] * n for i in range(n)]
    occd = [[0] * n for i in range(n)]  # represent tiles already with endpoint or bomb
    for i in range(n):
        for j in range(n):
            rando = rng_grader.uniform(0, 1)
            if rando < bd:
                bombs[i][j] = 1
                occd[i][j] = 1

    # generate random endpoints on the edge

    # generate edge coordinates
    edge_coord = (
        [[0, i] for i in range(0, n - 1)]
        + [[i, n - 1] for i in range(0, n - 1)]
        + [[n - 1, i] for i in range(1, n)]
        + [[i, 0] for i in range(1, n)]
    )
    pairs = []
    for _ in range(p):
        good_coord = []
        for randY, randX in edge_coord:
            if occd[randY][randX] == 0:
                good_coord.append([randY, randX])
        randY1, randX1 = rng_grader.choice(good_coord)
        occd[randY1][randX1] = 1
        good_coord.remove([randY1, randX1])
        randY2, randX2 = rng_grader.choice(good_coord)
        occd[randY2][randX2] = 1
        pairs.append([[randY1, randX1], [randY2, randX2]])

    # check to make sure pairs are connected
    # generate plan with all roads and check that report passes

    fullPlan = [[1] * n for i in range(n)]

    succ, score = analyzeRoadPlan(fullPlan, pairs, bombs)
    if not succ:
        # try again lol
        return generateSetup(n, p, bd)

    return pairs, bombs


def analyzeRoadPlan(plan, pairs, bombs):
    n = len(bombs)
    p = len(pairs)

    roadsBuilt = 0  # score
    realRoads = [[0] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            if plan[i][j] != 0:
                roadsBuilt += 1
                if bombs[i][j] == 0:
                    realRoads[i][j] = 1

    # essentially a "connected component search"
    # full search a component, rooted at arbitrary unsearched endpoint
    # verify that for each pair, either both or none of the endpoints appeared in that component
    # continue until all endpoints have been found

    visRoads = [[0] * n for i in range(n)]

    for pairNum in range(p):
        root = pairs[pairNum][0]
        if visRoads[root[0]][root[1]] == 1:
            continue

        dfsComponent(root[0], root[1], n, realRoads, visRoads)

        # ensure no components got split up
        for pairNum2 in range(p):
            pt1 = pairs[pairNum2][0]
            pt2 = pairs[pairNum2][1]
            if visRoads[pt1[0]][pt1[1]] != visRoads[pt2[0]][pt2[1]]:
                return False, n * n

        # check we actually visited the root (that there is a road on the root)
        if visRoads[root[0]][root[1]] == 0:
            return False, n * n

    return True, roadsBuilt


def dfsComponent(x, y, n, roads, visRoads):
    if x < 0 or x >= n or y < 0 or y >= n:
        return
    if roads[x][y] != 1:
        return
    if visRoads[x][y] == 1:
        return
    visRoads[x][y] = 1
    dfsComponent(x - 1, y, n, roads, visRoads)
    dfsComponent(x + 1, y, n, roads, visRoads)
    dfsComponent(x, y - 1, n, roads, visRoads)
    dfsComponent(x, y + 1, n, roads, visRoads)


soln = Planner()
pairs, bombs = generateSetup(n, p, bd)

runGrader(soln, pairs, bombs)
