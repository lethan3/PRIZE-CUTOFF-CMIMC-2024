import random
from PIL import Image
import string
import copy

class Planner:
    def setup(self, pairs, bd):
        self.n = 16
        self.pairs = pairs
        self.bd = bd
        self.yeetProbability = 0.07  # probability of removing a road
        self.bestPlan = [[1] * self.n for i in range(self.n)]
        self.sentPlan = []
        self.border_width = 0
        self.line_width = 0
        self.good_border = False
        self.good_line = False
        self.necessary = []
        self.tiles = None
        self.grid = None
        self.restart = False
        self.tolerance = 1
        self.width_tolerance = 0.5
        return
    
    def load_png(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        assert width == 16 and height == 16, "Image must be 16x16"
        tiles = []
        visted = [[False for i in range(16)] for j in range(16)]
        names = string.ascii_lowercase+string.ascii_uppercase+string.digits
        idx = 0

        for y in range(0, height):
            for x in range(0, width):
                if not visted[y][x]:
                    color = image.getpixel((x, y))
                    section = []
                    stack = [(y, x)]
                    while stack:
                        y1, x1 = stack.pop()
                        if x1 < 0 or x1 >= width or y1 < 0 or y1 >= height or visted[y1][x1] or image.getpixel((x1, y1)) != color:
                            continue
                        visted[y1][x1] = True
                        section.append((y1, x1))
                        stack.append((y1 + 1, x1))
                        stack.append((y1 - 1, x1))
                        stack.append((y1, x1 + 1))
                        stack.append((y1, x1 - 1))
                    tiles.append(section)
                    for y1, x1 in section:
                        visted[y1][x1] = names[idx]
                    idx += 1
                    idx %= len(names)
        
        for k in visted:
            print(*k)

        for k in tiles:
            print(*k)
        self.tiles = tiles
        self.grid = visted
    
    #*######## LINE FUNCTIONS #########
    def lerp(self, city1, city2, width, tolerance=2, width_tolerance=0.5):
        grid = [[0] * self.n for i in range(self.n)]
        #calculate line with ax + by + c = 0
        a = city2[1] - city1[1]
        b = city1[0] - city2[0]
        c = -a * city1[0] - b * city1[1]

        assert a * city1[0] + b * city1[1] + c == 0
        assert a * city2[0] + b * city2[1] + c == 0

        minx = min(city1[0], city2[0])
        maxx = max(city1[0], city2[0])
        miny = min(city1[1], city2[1])
        maxy = max(city1[1], city2[1])

        for i in range(self.n):
            for j in range(self.n):
                # distance(ax + by + c, (x0,y0)) = |ax0 + by0 + c|/√(a^2 + b^2)
                dist = abs(a * i + b * j + c) / ((a ** 2 + b ** 2) ** 0.5)
                
                #make sure point is within bewteen the two cities with some tolerance
                if minx - tolerance <= i <= maxx + tolerance and miny - tolerance <= j <= maxy + tolerance:
                    if dist-width_tolerance <= width/2:
                        grid[i][j] = 1
        return grid
    
    def lerp_manhatt(self, city1, city2, width, tolerance=1, width_tolerance=0.5):
        grid = [[0] * self.n for i in range(self.n)]
        
        if(city1[0] < city2[0]):
            city1, city2 = city2, city1

        cur = city1
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while cur[0] != city2[0] or cur[1] != city2[1]:
            min_dist = 100000
            min_dir = None
            for dir in directions:
                new_city = (cur[0] + dir[0], cur[1] + dir[1])
                #check if new city is within bounds
                if new_city[0] < 0 or new_city[0] >= self.n or new_city[1] < 0 or new_city[1] >= self.n:
                    continue
                dist = (new_city[0] - city2[0]) ** 2 + (new_city[1] - city2[1]) ** 2
                if dist < min_dist:
                    min_dist = dist
                    min_dir = dir
            cur = [cur[0] + min_dir[0], cur[1] + min_dir[1]]
            grid[cur[0]][cur[1]] = 1

        #go through the grid and padding the road with width
        newgrid = copy.deepcopy(grid)
        for i in range(self.n):
            for j in range(self.n):
                if grid[i][j] == 1:
                    for k in range(-width//2, width//2):
                        for l in range(-width//2, width//2):
                            if i + k < 0 or i + k >= self.n or j + l < 0 or j + l >= self.n:
                                continue
                            newgrid[i + k][j + l] = 1
        return newgrid

    def right_angle_path(self, city1, city2, width, tolerance=1, width_tolerance=0.5):
        grid = [[0] * self.n for i in range(self.n)]
        if city1[0] > city2[0]:
            city1, city2 = city2, city1
        x1, y1 = city1
        x2, y2 = city2
        
        for x in range(x1, x2 + 1 + width//2):
            for yy in range((-width+1)//2, width//2+1):
                y = y1 + yy
                if y < 0 or y >= self.n or x < 0 or x >= self.n:
                    continue
                grid[x][y] = 1
        for y in range(min(y1,y2), max(y1,y2) + 1):
            for xx in range((-width+1)//2, width//2+1):
                x = x2 + xx
                if x < 0 or x >= self.n:
                    continue
                grid[x][y] = 1

        return grid
    
    def random_path(self, city1, city2, width, tolerance=1, width_tolerance=0.5):
        grid = [[0] * self.n for i in range(self.n)]
        if city1[0] > city2[0]:
            city1, city2 = city2, city1
        x1, y1 = city1
        x2, y2 = city2
        
        cur = city1.copy()
        while cur[0] != city2[0] or cur[1] != city2[1]:
            grid[cur[0]][cur[1]] = 1
            if cur[0] == city2[0]:
                if y1 < y2:
                    cur[1] += 1
                else:
                    cur[1] -= 1
                continue
            if cur[1] == city2[1]:
                cur[0] += 1
                continue
            r = random.randint(0, 1)
            if r == 0:
                cur[0] += 1
            else:
                if y1 < y2:
                    cur[1] += 1
                else:
                    cur[1] -= 1
        
        grid[cur[0]][cur[1]] = 1
        
        newgrid = copy.deepcopy(grid)
        for i in range(self.n):
            for j in range(self.n):
                if grid[i][j] == 1:
                    for k in range(-width//2, width//2):
                        for l in range(-width//2, width//2):
                            if i + k < 0 or i + k >= self.n or j + l < 0 or j + l >= self.n:
                                continue
                            newgrid[i + k][j + l] = 1
        return newgrid

    def bresenham(self, city1, city2): 
        #TODO
        ...

    #*######## BORDER FUNCTIONS #########
    
    def rand_dist_from_border(self, dist):
        dist = random.randint(1, dist)
        r = random.randint(0, 3)
        if (r == 0):
            return (dist - 1, random.randint(dist - 1, self.n - dist))
        elif (r == 1):
            return (self.n - dist, random.randint(dist - 1, self.n - dist))
        elif (r == 2):
            return (random.randint(dist - 1, self.n - dist), dist - 1)
        else:
            return (random.randint(dist - 1, self.n - dist), self.n - dist)
        
    def border_roads(self, plan):
        roads = []
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for i in range(self.n):
            for j in range(self.n):
                if plan[i][j] == 1:
                    for dir in dirs:
                        x, y = i + dir[0], j + dir[1]
                        if x < 0 or x >= self.n or y < 0 or y >= self.n:
                            roads.append((i, j))
                            break
                        if plan[x][y] == 0:
                            roads.append((i, j))
                            break

        return roads

    
    def generate_border(self, width):
        plan = [[0] * self.n for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if (i < width or self.n - i <= width) or (j < width or self.n - j <= width):
                    plan[i][j] = 1
        return plan
    

    #*######## TRIMMING FUNCTIONS #########
    def remove_islands(self, sentPlan):
        plan = [[0] * self.n for i in range(self.n)]
        #flood fill from city1
        stack = [self.pairs[i][0] for i in range(len(self.pairs))]
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= self.n or y < 0 or y >= self.n or plan[x][y] == 1:
                continue
            if sentPlan[x][y] == 0:
                continue
            plan[x][y] = 1
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))
        return plan
    
    def remove_branches(self, sentPlan):
        tips = []
        for i in range(self.n):
            for j in range(self.n):
                if sentPlan[i][j] == 1:
                    count = 0
                    for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                        if x < 0 or x >= self.n or y < 0 or y >= self.n:
                            continue
                        if sentPlan[x][y] == 1:
                            count += 1
                    if count == 1:
                        tips.append((i, j))
        while len(tips) > 0:
            i, j = tips.pop()
            sentPlan[i][j] = 0
            for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if x < 0 or x >= self.n or y < 0 or y >= self.n:
                    continue
                if sentPlan[x][y] == 1:
                    count = 0
                    for xx, yy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                        if xx < 0 or xx >= self.n or yy < 0 or yy >= self.n:
                            continue
                        if sentPlan[xx][yy] == 1:
                            count += 1
                    if count == 1:
                        tips.append((x, y))
        return sentPlan
    
    #*######## UTIL FUNCTIONS #########

    def combine(self, plan1, plan2):
        plan = [[0] * self.n for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                plan[i][j] = plan1[i][j] or plan2[i][j]
        return plan
    
    def rand_bool(self, probability):
        return 1 if random.random() < probability else 0

    def check_connected(self, target_pair, current_plan):
        vis = [[0 for i in range(self.n)] for j in range(self.n)]
        queue = [target_pair[0]]
        while len(queue):
            current_pair = queue.pop(0)
            if vis[current_pair[0]][current_pair[1]]:
                continue
            vis[current_pair[0]][current_pair[1]] = 1
            for x in range(-1,2):
                for y in range(-1, 2):
                    if abs(x + y) == 1 and 0 <= current_pair[0] + x < self.n and 0 <= current_pair[1] + y < self.n and current_plan[current_pair[0] + x][current_pair[1] + y] != 0:
                        next_pair = (current_pair[0] + x, current_pair[1] + y)
                        if next_pair == target_pair[1]:
                            return True
                        queue.append(next_pair)
        return False

    def count_ones (self, current_plan):
        counter = 0
        for i in range(self.n):
            for j in range(self.n):
                if current_plan[i][j] != 0:
                    counter += 1
        return counter
    

    #*######## STRATEGY FUNCTIONS #########

    def shave_from_border_v2(self, q, queryOutputs):
        if not self.good_border:
            if len(queryOutputs) == 0 or not queryOutputs[-1]:
                self.border_width += 1
                self.sentPlan = self.generate_border(self.border_width)
                return self.sentPlan
            else:
                self.good_border = True

        if queryOutputs[-1]:
            self.bestPlan = copy.deepcopy(self.sentPlan)
        else:
            self.necessary.append(self.last_rmv)
        
        self.sentPlan = copy.deepcopy(self.bestPlan)

        del_i, del_j = self.rand_dist_from_border(self.border_width)

        while not self.sentPlan[del_i][del_j] and not (del_i, del_j) in self.necessary:
            # print(del_i, del_j)
            del_i, del_j = self.rand_dist_from_border(self.border_width)

        self.sentPlan[del_i][del_j] = False
        self.last_rmv = (del_i, del_j)
        #flood fill from city1
        self.sentPlan = self.remove_islands(self.sentPlan)
        self.sentPlan = self.remove_branches(self.sentPlan)
        return self.sentPlan

    def shave_from_line(self, q, queryOutputs, line_func):
        if not self.good_line or q == 100 or self.restart:
            if len(queryOutputs) == 0 or not queryOutputs[-1] or self.restart:
                self.restart = False
                self.line_width += 1
                self.sentPlan = line_func(self.pairs[0][0], self.pairs[0][1], self.line_width, self.tolerance, self.width_tolerance)
                return self.sentPlan
            else:
                self.good_line = True

        if queryOutputs[-1]:
            self.bestPlan = copy.deepcopy(self.sentPlan)
        elif q <= 60:
            self.necessary+= self.last_rmv


        self.last_rmv = []  
        
        self.sentPlan = copy.deepcopy(self.bestPlan)


        #print(*self.sentPlan, sep='\n')

        points_on_border = self.border_roads(self.sentPlan)
        #print(points_on_border)

        for i in range((2 if q > 60 else 1)):
            del_i, del_j = random.choice(points_on_border)
            
            while not self.sentPlan[del_i][del_j] and not (del_i, del_j) in self.necessary and not (del_i, del_j) == tuple(self.pairs[0][0]) and not (del_i, del_j) == tuple(self.pairs[0][1]):
                # print(del_i, del_j)
                del_i, del_j = random.choice(points_on_border)

            self.sentPlan[del_i][del_j] = False
            self.last_rmv.append( (del_i, del_j) )

        self.sentPlan = self.remove_islands(self.sentPlan)
        #self.sentPlan = self.remove_branches(self.sentPlan)
        return self.sentPlan
    
    def random_blossom(self, q, queryOutputs):
        plan = [[0 for i in range(self.n)] for j in range(self.n)]
        INF = 1e9 + 7
        PROB_CONST = 8
        grid_counter = 0
        while True:
            grid_counter += 1
            #print(grid_counter)
            #hopefully generate a valid grid with around 80-90 squares
            for i in range(self.n):
                for j in range(self.n):
                    dist = INF
                    for v in self.pairs:
                        dist = min(dist, abs(i - v[0][0]) + abs(j - v[0][1]))
                        dist = min(dist, abs(i - v[1][0]) + abs(j - v[1][1]))
                    #lower likelihood of being a 1 if min distance is further...
                    plan[i][j] = 1 if dist == 0 else self.rand_bool(PROB_CONST/dist)
            valid_grid = 1
            #check that the grid is valid at the moment, otherwise generate the grid again
            for v in self.pairs:
                if not self.check_connected(v, plan):
                    #print(v)
                    valid_grid = 0
            if not valid_grid:
                continue
            pair_counter = 2
            #print(self.count_ones(plan))
            for v in self.pairs:
                plan[v[0][0]][v[0][1]] = pair_counter
                plan[v[1][0]][v[1][1]] = pair_counter
                pair_counter += 1
            #for i in range(self.n):
                #print(" ".join(list([str(v) for v in plan[i]])))

            #assuming the grid is valid, prune out the nodes that are obviously not useful (this is anything with degree <= 1 that is not an endpoint)

            break
        return plan
    

    #*########## main task functions here #########


    def task1(self, q, queryOutputs):  # p = 5, bd = 0.25
        return self.shave_from_border_v2(q, queryOutputs)

    def task2(self, q, queryOutputs): # p = 5, bd = 0.1
        return self.task1(q, queryOutputs)

    def task3(self, q, queryOutputs): # p = 1, bd = 0.25
        return self.shave_from_line(q, queryOutputs, self.random_path)


    def task4(self, q, queryOutputs): # p = 1, bd = 0.1
        return self.shave_from_line(q, queryOutputs, self.random_path)

            
    def task4_same_row(self, q):
        ...
        # return plan
    def theoretical_max(self, q, queryOutputs):
        return self.random_path(self.pairs[0][0], self.pairs[0][1], 2)
        # draw right angle between the two points
        
        return self.right_angle_path(self.pairs[0][0], self.pairs[0][1], 3)

    def query(self, q, queryOutputs):
        # feel free to modify this function, this is just a suggestion
        if len(self.pairs) == 5 and self.bd == 0.25:
            return self.task1(q, queryOutputs)
        # if len(self.pairs) == 5 and self.bd == 0.25:
        #     return self.task1(q, queryOutputs)
        
        if len(self.pairs) == 5 and self.bd == 0.1:
            return self.task2(q, queryOutputs)
        
        if len(self.pairs) == 1 and self.bd == 0.25:
            return self.task3(q, queryOutputs)
        
        if len(self.pairs) == 1 and self.bd == 0.1:
            return self.task4(q, queryOutputs)
        
        if len(self.pairs) == 1 and self.bd == 0:
            return self.theoretical_max(q, queryOutputs)
        
