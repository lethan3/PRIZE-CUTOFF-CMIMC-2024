import random
from PIL import Image
import string

class Planner:
    def setup(self, pairs, bd):
        self.n = 16
        self.pairs = pairs
        self.bd = bd
        self.yeetProbability = 0.07  # probability of removing a road
        self.bestPlan = [[1] * self.n for i in range(self.n)]
        self.sentPlan = []
        self.border_width = 0
        self.good_border = False
        self.necessary = []
        self.tiles = None
        self.grid = None
        return
    
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


    def task1(self, q, queryOutputs):  # p = 5, bd = 0.25
        if not self.good_border:
            if len(queryOutputs) == 0 or not queryOutputs[-1]:
                self.border_width += 1
                self.sentPlan = [[0] * self.n for i in range(self.n)]

                for i in range(self.n):
                    for j in range(self.n):
                        if (i < self.border_width or self.n - i <= self.border_width) or (j < self.border_width or self.n - j <= self.border_width):
                            self.sentPlan[i][j] = 1
                return self.sentPlan
            else:
                self.good_border = True

        if queryOutputs[-1]:
            self.bestPlan = [[self.sentPlan[i][j] for j in range(self.n)] for i in range(self.n)]
        else:
            self.necessary.append(self.last_rmv)
        
        self.sentPlan = [[self.bestPlan[i][j] for j in range(self.n)] for i in range(self.n)]

        del_i, del_j = self.rand_dist_from_border(self.border_width)

        while not self.sentPlan[del_i][del_j] and not (del_i, del_j) in self.necessary:
            # print(del_i, del_j)
            del_i, del_j = self.rand_dist_from_border(self.border_width)

        self.sentPlan[del_i][del_j] = False
        self.last_rmv = (del_i, del_j)
        return self.sentPlan

        # # print(queryOutputs)
        # l = len(queryOutputs)
        # if l > 0 and queryOutputs[l - 1]:
        #     self.bestPlan = self.sentPlan
        # n = self.n
        # newPlan = [[1] * n for i in range(n)]

        # # take the most recent successful plan
        # # remove each road with small probability
        # for i in range(n):
        #     for j in range(n):
        #         newPlan[i][j] = self.bestPlan[i][j]
        #         if newPlan[i][j] == 1:
        #             rando = random.uniform(0, 1)
        #             if rando < self.yeetProbability:
        #                 newPlan[i][j] = 0

        # self.sentPlan = newPlan
        # return self.sentPlan

    def task2(self, q, queryOutputs): # p = 5, bd = 0.1
        return self.task1(q, queryOutputs)

    def task3(self, q, queryOutputs): # p = 1, bd = 0.25
        return self.task1(q, queryOutputs)


    

    def task4(self, q, queryOutputs): # p = 1, bd = 0.1
        # check if pairs are in the same row or column
        if (q==2): return self.lerp(self.pairs[0][0], self.pairs[0][1], 2, 1)
        if (q==1): return self.lerp(self.pairs[0][0], self.pairs[0][1], 1, 0)


        return self.task1(q, queryOutputs)

        if self.pairs[0][0][0] == self.pairs[0][1][0] or self.pairs[0][0][1] == self.pairs[0][1][1]:
            return self.task4_same_row(q)
            
    def task4_same_row(self, q):
        ...
        # return plan

    def theoretical_max(self, q, queryOutputs):
        x1, y1 = self.pairs[0][0]
        x2, y2 = self.pairs[0][1]
        # draw right angle between the two points
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        plan = [[0] * self.n for i in range(self.n)]
        if q%4 == 1:
            for i in range(x1, x2 + 1):
                plan[i][y1] = 1
            for i in range(y1, y2 + 1):
                plan[x2][i] = 1
        elif q%4 == 2:
            for i in range(x1, x2 + 1):
                plan[i][y2] = 1
            for i in range(y1, y2 + 1):
                plan[x1][i] = 1
        elif q%4 == 3:
            for i in range(x1, x2 + 1):
                plan[i][y2] = 1
            for i in range(y1, y2 + 1):
                plan[x2][i] = 1
        else:
            for i in range(x1, x2 + 1):
                plan[i][y1] = 1
            for i in range(y1, y2 + 1):
                plan[x1][i] = 1
        return plan

    def query(self, q, queryOutputs):
        # feel free to modify this function, this is just a suggestion
        if len(self.pairs) == 5 and self.bd == 0.25:
            return self.task1(q, queryOutputs)
        
        if len(self.pairs) == 5 and self.bd == 0.1:
            return self.task2(q, queryOutputs)
        
        if len(self.pairs) == 1 and self.bd == 0.25:
            return self.task3(q, queryOutputs)
        
        if len(self.pairs) == 1 and self.bd == 0.1:
            return self.task4(q, queryOutputs)
        
        if len(self.pairs) == 1 and self.bd == 0:
            return self.theoretical_max(q, queryOutputs)
        
