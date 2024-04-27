"""
Edit this file! This is the file you will submit.
"""

import random

"""
NOTE: Each soldier's memory in the final runner will be separate from the others.

WARNING: Do not print anything to stdout. It will break the grading script!
"""

def boids(ally: list, enemy: list, offset: int) -> int:
    SEPERATION_WEIGHT = 1
    COHESION_WEIGHT = 1
    netforce = 0
    
    left_sep = ally[0] + ally[1]
    right_sep = ally[5] + ally[6]
    cohesion = ally[2] + ally[3] + ally[4]
    left_sep = left_sep/sum(ally)
    right_sep = right_sep/sum(ally)
    cohesion = cohesion/sum(ally)

    netforce += -left_sep*SEPERATION_WEIGHT + right_sep*SEPERATION_WEIGHT + cohesion*COHESION_WEIGHT
    netforce *= 3
    print(netforce)

    if offset == 0:
        netforce /= 3
    if offset == 1:
        netforce+= 1
    if offset == -1:
        netforce-= 1

    netforce += random.uniform(-1,1)
    if netforce > 1:
        return 1
    if netforce < -1:
        return -1
    return 0

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
        if(i==3): netforce += max(0,ally[3]-6)*(random.random()*2-1)
    #print(netforce)
    #normalize netforce
    #print(netforce)
    netforce += offset
    if(netforce>1): return 1
    elif(netforce < -1): return -1
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

def lol2electricboogaloo(ally: list, enemy: list, offset: int) -> int:
    castle_idx = 3+offset
    castle_dif = ally[castle_idx] - enemy[castle_idx]
    SOLDIER_CAP = 7
    SAFE_PADDING = 1
    CASTLE_DIF_CAP = 6
    if (offset == 0):
        
        if enemy[3] > SOLDIER_CAP: # some max number before its not worth to win
            return random.choice([-1, 1])

        elif castle_dif > CASTLE_DIF_CAP: # some max number before its not worth to spend that much
            return random.choice([0]*(ally[3]-castle_dif+1)+[1]*((castle_dif-2)//2)+[-1]*((castle_dif-2)//2)) # send away a few soldiers
        
        else:
            return 0
    
    if (offset == 1): 
        if enemy[castle_idx] > SOLDIER_CAP:
            return -1
        
        elif castle_dif >= SAFE_PADDING:
            return -1
        
        else:
            return 1
    
    if (offset == -1):
        if enemy[castle_idx] > SOLDIER_CAP:
            return 1
        
        elif castle_dif >= SAFE_PADDING:
            return 1
        
        else:
            return -1
        
def lol2electricboogalootest(ally: list, enemy: list, offset: int, SOLDIER_CAP,SAFE_PADDING,CASTLE_DIF_CAP) -> int:
    castle_idx = 3+offset
    castle_dif = ally[castle_idx] - enemy[castle_idx]

    if (offset == 0):
        
        if enemy[3] > SOLDIER_CAP: # some max number before its not worth to win
            return random.choice([-1, 1])

        elif castle_dif > CASTLE_DIF_CAP: # some max number before its not worth to spend that much
            return random.choice([0]*(ally[3])+[1]*((castle_dif-2)//2)+[-1]*((castle_dif-2)//2)) # send away a few soldiers
        
        else:
            return 0
    
    if (offset == 1): 
        if enemy[castle_idx] > SOLDIER_CAP:
            return -1
        
        elif castle_dif >= SAFE_PADDING:
            return -1
        
        else:
            
            return 1
    
    if (offset == -1):
        if enemy[castle_idx] > SOLDIER_CAP:
            return 1
        
        elif castle_dif >= SAFE_PADDING:
            return 1
        
        else:
            return -1
test = 0

def lol2electricboogalooV2(ally: list, enemy: list, offset: int) -> int:
    castle_idx = 3+offset
    castle_dif = ally[castle_idx] - enemy[castle_idx]
    SOLDIER_CAP = 7
    SAFE_PADDING = 1
    CASTLE_DIF_CAP = 6
    if (offset == 0):
        
        if enemy[3] > SOLDIER_CAP: # some max number before its not worth to win
            return random.choice([-1, 1])

        elif castle_dif > CASTLE_DIF_CAP: # some max number before its not worth to spend that much
            return random.choice([0]*ally[3]+[1]*((castle_dif-2)//2)+[-1]*((castle_dif-2)//2)) # send away a few soldiers
        
        else:
            return 0
    
    if (offset == 1): 
        if enemy[castle_idx] > SOLDIER_CAP:
            return -1
        
        elif castle_dif >= SAFE_PADDING:
            return -1
        
        else:
            return (1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < (-2*castle_dif)+2 else -1)
    
    if (offset == -1):
        if enemy[castle_idx] > SOLDIER_CAP:
            return 1
        
        elif castle_dif >= SAFE_PADDING:
            return 1
        
        else:
            return (-1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < -2*castle_dif+2 else 1)

def lol2electricboogalooV3(ally: list, enemy: list, offset: int) -> int:
    castle_idx = 3+offset
    castle_dif = ally[castle_idx] - enemy[castle_idx]
    SOLDIER_CAP = 10
    SOLDIER_CAP_CAP= 15
    SAFE_PADDING = 1
    CASTLE_DIF_CAP = 6
    if (offset == 0):
        
        if enemy[3] > SOLDIER_CAP: # some max number before its not worth to win
            left_castle_dif = ally[0]-enemy[0]
            right_castle_dif = ally[6]-enemy[6]
            if enemy[0] > SOLDIER_CAP_CAP and enemy[6] > SOLDIER_CAP_CAP:
                return random.choice([-1, 1])
            elif enemy[0] > SOLDIER_CAP_CAP:
                return 1
            elif enemy[6] > SOLDIER_CAP_CAP:
                return -1
            elif left_castle_dif < 0 and right_castle_dif < 0:
                return random.choice([-1]*(-left_castle_dif+4)+[1]*(-right_castle_dif+4))
            elif left_castle_dif < 0:
                return -1
                return random.choice([-1]*(-left_castle_dif+4)+[1]*max(0,(SAFE_PADDING-right_castle_dif)))
            elif right_castle_dif < 0:
                return 1
                return random.choice([-1]*max(0,(SAFE_PADDING-left_castle_dif))+[1]*(-right_castle_dif+4))
            else:
                return random.choice([-1, 1])


        elif castle_dif > CASTLE_DIF_CAP: # some max number before its not worth to spend that much
            return random.choice([0]*ally[3]+[1]*((castle_dif-2)//2)+[-1]*((castle_dif-2)//2)) # send away a few soldiers
        
        else:
            return 0
    
    if (offset == 1): 
        if enemy[castle_idx] > SOLDIER_CAP:
            return -1
        
        elif castle_dif >= SAFE_PADDING:
            return -1
        
        else:
            return (1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < (-castle_dif)+2 else -1)
    
    if (offset == -1):
        if enemy[castle_idx] > SOLDIER_CAP:
            return 1
        
        elif castle_dif >= SAFE_PADDING:
            return 1
        
        else:
            return (-1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < -castle_dif+2 else 1)
        
def lol2electricboogalooV4(ally: list, enemy: list, offset: int) -> int:
    castle_idx = 3+offset
    castle_dif = ally[castle_idx] - enemy[castle_idx]
    SOLDIER_CAP = 7
    SOLDIER_CAP_CAP= 15
    SAFE_PADDING = 2
    CASTLE_DIF_CAP = 6
    if (offset == 0):
        
        if enemy[3] > SOLDIER_CAP: # some max number before its not worth to win
            left_castle_dif = ally[0]-enemy[0]
            right_castle_dif = ally[6]-enemy[6]
            if enemy[0] > SOLDIER_CAP_CAP and enemy[6] > SOLDIER_CAP_CAP:
                return 0
            elif left_castle_dif < 0 and right_castle_dif < 0:
                return random.choice([-1]*(-left_castle_dif+4)+[1]*(-right_castle_dif+4))
            elif left_castle_dif < 0:
                return random.choice([-1]*(-left_castle_dif+4)+[1]*max(0,(SAFE_PADDING-right_castle_dif)))
            elif right_castle_dif < 0:
                return random.choice([-1]*max(0,(SAFE_PADDING-left_castle_dif))+[1]*(-right_castle_dif+4))
            else:
                return random.choice([-1, 1])


        elif castle_dif > CASTLE_DIF_CAP: # some max number before its not worth to spend that much
            return random.choice([0]*ally[3]+[1]*((castle_dif-2)//2)+[-1]*((castle_dif-2)//2)) # send away a few soldiers
        
        else:
            return 0
    
    if (offset == 1): 
        if enemy[castle_idx] > SOLDIER_CAP:
            return -1
        
        elif castle_dif >= SAFE_PADDING:
            return -1
        
        else:
            return (1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < (-castle_dif)+2 else -1)
    
    if (offset == -1):
        if enemy[castle_idx] > SOLDIER_CAP:
            return 1
        
        elif castle_dif >= SAFE_PADDING:
            return 1
        
        else:
            return (-1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < -castle_dif+2 else 1)

def set_n_per_castle(ally: list, enemy: list, offset: int) -> int:
    N = 9
    CUT_OFF = 5
    castle_idx = 3+offset
    if (offset == 0):
        if ally[castle_idx]+ally[castle_idx-1]+ally[castle_idx+1] <= CUT_OFF:
            return random.randint(-1, 1)
        elif ally[castle_idx] <= N:
            return 0
        else:
            if random.randint(0,ally[castle_idx]) < ally[castle_idx]-N:
                return random.randint(-1, 1)
            else:
                return 0
    if (offset == 1):
        if ally[castle_idx] >= N:
            return -1
        elif ally[castle_idx]+ally[castle_idx-1]+ally[castle_idx+1] <= CUT_OFF:
            return random.choice([-1,-1,1])
        else:
            return 1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < N-ally[castle_idx] else -1
    if (offset == -1):
        if ally[castle_idx] >= N:
            return 1
        elif ally[castle_idx]+ally[castle_idx-1]+ally[castle_idx+1] <= CUT_OFF:
            return random.choice([-1,1,1])
        else:
            return -1 if random.randint(0,ally[castle_idx+1]+ally[castle_idx-1]) < N-ally[castle_idx] else 1

def move_clockwise(ally: list, enemy: list, offset: int) -> int:
    #move clockwise until you have at least 8, then try to stay; if not on a castle pause with probability relative to the number of peolpe on your cell
    SECURED_MAX = 11 #leave cell with probability relative to the number of squares > 11
    SECURED_CONST = 8
    MOVE_CONST = 4
    castle_idx = 3 + offset
    if offset == 0:
        #on castle
        if ally[castle_idx] < enemy[castle_idx] and ally[castle_idx] >= SECURED_MAX:
            #we will not lose a castle with 11+ people on it
            return 1
        else:
            left_side = ally[castle_idx - 1] + ally[castle_idx-2]
            if enemy[castle_idx] > ally[castle_idx] and left_side == 0 and (ally[castle_idx - 3] == 0 or enemy[castle_idx - 3] < ally[castle_idx - 3]): #they arent coming to help :pensive:
                return 1
            elif enemy[castle_idx] > ally[castle_idx] and enemy[castle_idx + 3] > ally[castle_idx + 3] and enemy[castle_idx - 3] > ally[castle_idx - 3]: #we havent captured enough castles, so good idea to wait
                return 0
            elif enemy[castle_idx] - ally[castle_idx] > MOVE_CONST or (ally[castle_idx] <= enemy[castle_idx] and ally[castle_idx + 3] <= enemy[castle_idx + 3] and ally[castle_idx + 3] > 0): #help a neighbor
                return 1
            elif ally[castle_idx] > enemy[castle_idx] and ally[castle_idx] > SECURED_MAX:
                if random.randint(1, max(2, 2 * (SECURED_MAX + 1) - ally[castle_idx])) == 1:
                    return 1
                else:
                    return 0
            else:
                return 0
    if ally[3] > SECURED_CONST:
        return 1
    if ally[castle_idx] < SECURED_CONST:
        #stop to collect others
        if 0 < ally[2] < ally[3] and offset != 2:
            return 0
        elif 0 < ally[1] < ally[3] and offset == 2:
            return 0
        else:
            return 1


    return 1
def get_strategies():
    """
    Returns a list of strategies to play against each other.

    In the local tester, all of the strategies will be used as separate players, and the 
    pairwise winrate will be calculated for each strategy.

    In the official grader, only the first element of the list will be used as your strategy.
    """
    # strategies = [move_clockwise,lol2electricboogalooV2,lol2electricboogaloo,lol,offset]
    strategies = [move_clockwise, lol2electricboogalooV2]

    # strategies = [move_clockwise, offset]

    #strategies.append(lambda ally, enemy, offset: lol2electricboogalootest(ally, enemy, offset, 7, 1, 5))
    #strategies.append(lambda ally, enemy, offset: lol2electricboogalootest(ally, enemy, offset, 7, 2, 6))
    #strategies.append(lambda ally, enemy, offset: lol2electricboogalootest(ally, enemy, offset, 7, 2, 5))
    #strategies.append(lambda ally, enemy, offset: lol2electricboogalootest(ally, enemy, offset, 8, 2, 5))
    

    return strategies
