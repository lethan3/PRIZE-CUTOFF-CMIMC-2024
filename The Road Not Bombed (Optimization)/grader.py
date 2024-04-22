import random
from strategy import Planner
import time
import argparse
import math
import copy

"""
Modify the parameters below for different tasks
"""

# Task 1: p = 5, bd = 0.25
#p = 5  # number of cities
#bd = 0.25  # bomb density

# Task 2: p = 5, bd = 0.1
# p = 5 # number of cities
# bd = 0.1 # bomb density

# Task 3: p = 1, bd = 0.25
# p = 1 # number of cities
# bd = 0.25 # bomb density

# Task 4: p = 1, bd = 0.1
p = 1 # number of cities
bd = 0.1 # bomb density

rng_grader = random.Random()  # use this for generating fixed setup
rng_grader.seed(time.time())

VERBOSE = False  # print more details
LAST = True  # whether to print the last query made in each TC
NOTHING = False
GEO_SCORE = 0
TRUEGEO_SCORE = 1
AVG_SCORE = 0
n = 16  # board size is n*n
q = 100  # number of queries


def runGrader(soln, pairs, bombs):
    global GEO_SCORE, AVG_SCORE, TRUEGEO_SCORE
    # pairs represented as array of length p, each element is a length 2 array of length 2 array of coordinates
    # bombs represented with n*m array, '1' denotes bomb, '0' denotes no bomb
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
    if not NOTHING: print(f"Best score: {bestScore}")
    GEO_SCORE += math.log2(bestScore)
    TRUEGEO_SCORE *= bestScore
    AVG_SCORE += bestScore
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

def shortest_path_length(pairs, bombs):
    n = len(bombs)
    p = len(pairs)
    roadsBuilt = 0  # score
    visited = copy.deepcopy(bombs)
    cur = [pairs[0][0],1]
    visited[cur[0][0]][cur[0][1]] = 1
    queue = [cur]
    while len(queue) > 0:
        cur = queue.pop(0)
        x, y = cur[0]
        if x == pairs[0][1][0] and y == pairs[0][1][1]:
            return cur[1]
        if x > 0 and visited[x-1][y] == 0:
            queue.append([[x-1, y], cur[1]+1])
            visited[x-1][y] = 1
        if x < n-1 and visited[x+1][y] == 0:
            queue.append([[x+1, y], cur[1]+1])
            visited[x+1][y] = 1
        if y > 0 and visited[x][y-1] == 0:
            queue.append([[x, y-1], cur[1]+1])
            visited[x][y-1] = 1
        if y < n-1 and visited[x][y+1] == 0:
            queue.append([[x, y+1], cur[1]+1])
            visited[x][y+1] = 1
    return -1

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="The Road Not Bombed local runner CLI")

    parser.add_argument("--task", "-t", type=int, default=0, help="Task number (1-5) [5, 0.25], [5, 0.1], [1, 0.25], [1, 0.1], [1, 0]")
    parser.add_argument("--games", "-g", type=int, default=1, help="Number of games to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print more details")
    parser.add_argument("--silent", "-s", action="store_true", help="Don't print game states")
    parser.add_argument("--seed", "-sd", type=int, default=None, help="Random seed")
    parser.add_argument("--png", "-p", type=str, default=None, help="png file for strategy")
    parser.add_argument("--nothing", "-n", action="store_true", help="Only print final scores")
    parser.add_argument("--optimal", "-o", action="store_true", help="Gives average perfect solution if board is known")

    args = parser.parse_args()

    if args.seed:
        rng_grader.seed(args.seed)
    
    if args.optimal:
        p, bd = 1, 0.25
        GEO_SCORE = 0
        AVG_SCORE = 0
        TRUEGEO_SCORE = 1
        if args.games > 50:
            TRUEGEO_SCORE = 0

        for i in range(args.games):
            pairs, bombs = generateSetup(n, p, bd)
            length = shortest_path_length(pairs, bombs)
            AVG_SCORE += length
            GEO_SCORE += math.log2(length)
            TRUEGEO_SCORE *= length
        
        print(f"Total Games: {args.games}         Task: [1, 0.25]")
        print('\x1b[0;31;40m'+f"Average Score: {AVG_SCORE/args.games}"+'\x1b[0m')
        print('\x1b[0;31;40m'+f"Geometric Mean Score: {round(2**(GEO_SCORE/args.games),2)}"+'\x1b[0m')
        print('\x1b[0;31;40m'+f"True Geometric Mean Score: {round(TRUEGEO_SCORE**(1/args.games),2)}"+'\x1b[0m')
        print("-"*50)
        p, bd = 1, 0.1
        GEO_SCORE = 0
        AVG_SCORE = 0
        TRUEGEO_SCORE = 1
        if args.games > 50:
            TRUEGEO_SCORE = 0

        for i in range(args.games):
            pairs, bombs = generateSetup(n, p, bd)
            length = shortest_path_length(pairs, bombs)
            AVG_SCORE += length
            GEO_SCORE += math.log2(length)
            TRUEGEO_SCORE *= length
        
        print(f"Total Games: {args.games}         Task: [1, 0.1]")
        print('\x1b[0;31;40m'+f"Average Score: {AVG_SCORE/args.games}"+'\x1b[0m')
        print('\x1b[0;31;40m'+f"Geometric Mean Score: {round(2**(GEO_SCORE/args.games),2)}"+'\x1b[0m')
        print('\x1b[0;31;40m'+f"True Geometric Mean Score: {round(TRUEGEO_SCORE**(1/args.games),2)}"+'\x1b[0m')
        print("-"*50)
        exit()
    

    if args.nothing:
        NOTHING = True
        VERBOSE = False
        LAST = False

    if args.verbose:
        VERBOSE = True

    if args.silent:
        VERBOSE = False
        LAST = False

    tasks = []


    if args.task == 1:
        p = 5
        bd = 0.25
    elif args.task == 2:
        p = 5
        bd = 0.1
    elif args.task == 3:
        p = 1
        bd = 0.25
    elif args.task == 4:
        p = 1
        bd = 0.1
    elif args.task == 5:
        p = 1
        bd = 0  
    else:
        p = 1
        bd = 0.1
        tasks = [[5, 0.25], [5, 0.1], [1, 0.25]]
    tasks.append([p, bd])

    soln = Planner()

    

    if args.png:
        soln.load_png(args.png)

    for task in tasks:
        p, bd = task
        GEO_SCORE = 0
        AVG_SCORE = 0
        TRUEGEO_SCORE = 1
        if args.games > 50:
            TRUEGEO_SCORE = 0
        for i in range(args.games):
            if not NOTHING: print(f"Game {i+1}         Task: {task}")
            pairs, bombs = generateSetup(n, p, bd)
            runGrader(soln, pairs, bombs)
        print(f"Total Games: {args.games}         Task: {task}")
        print('\x1b[0;31;40m'+f"Average Score: {AVG_SCORE/args.games}"+'\x1b[0m')
        print('\x1b[0;31;40m'+f"Geometric Mean Score: {round(2**(GEO_SCORE/args.games),2)}"+'\x1b[0m')
        print('\x1b[0;31;40m'+f"True Geometric Mean Score: {round(TRUEGEO_SCORE**(1/args.games),2)}"+'\x1b[0m')
        print("-"*50)

        
