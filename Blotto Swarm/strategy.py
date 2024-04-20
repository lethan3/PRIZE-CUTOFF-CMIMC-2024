"""
Edit this file! This is the file you will submit.
"""

import random

"""
NOTE: Each soldier's memory in the final runner will be separate from the others.

WARNING: Do not print anything to stdout. It will break the grading script!
"""

def keep_2_per_castle(ally: list, enemy: list, offset: int) -> int:
    # Implement me!
    return 0


def go_to_nearby_castlev2(ally: list, enemy: list, offset: int) -> int:
    castle_idx = 3+offset
    return offset

def go_to_nearby_castle(ally: list, enemy: list, offset: int) -> int:
    return offset

def weighted_random(ally: list, enemy: list, offset: int) -> int:
    # Implement me!
    netforce = 0
    for i in range(len(ally)):
        if(i!=3): netforce -= ally[i]/((i-3)*abs(1-3))
        if(i==3): netforce += max(0,ally[3]-2)*(random.random()*2-1)
    
    #normalize netforce
   #print(netforce)
    netforce += offset
    if(netforce>1): return 1
    elif(netforce < -1): return -1
    else: return 0

def weighted_randomv2(ally: list, enemy: list, offset: int) -> int:
    # Implement me!
    if(ally[3]<3 and offset == 0): return 0

    netforce = 0
    for i in range(len(ally)):
        if(i!=3): netforce -= ally[i]/((i-3)*abs(1-3))
        if(i==3): netforce += max(0,ally[3]-4)*(random.random()*2-1)
    #print(netforce)
    #normalize netforce
    #print(netforce)
    netforce += offset
    if(netforce>0.5): return 1
    elif(netforce < -0.5): return -1
    else: return 0

def random_strategy(ally: list, enemy: list, offset: int) -> int:
    # A random strategy to use in your game
    return random.randint(-1, 1)

def offset(ally: list, enemy: list, offset: int) -> int:
    return offset

def lol(ally: list, enemy: list, offset: int) -> int:
    if (offset != 0): return 1
    if (offset == 0 and ally[3] > enemy[3] + 2):
        r = random.uniform(0, ally[3])
        return 1 if r < (ally[3] - 6) / 2 else 0
    return 0



def get_strategies():
    """
    Returns a list of strategies to play against each other.

    In the local tester, all of the strategies will be used as separate players, and the 
    pairwise winrate will be calculated for each strategy.

    In the official grader, only the first element of the list will be used as your strategy.
    """
    strategies = [lol, offset]

    return strategies
