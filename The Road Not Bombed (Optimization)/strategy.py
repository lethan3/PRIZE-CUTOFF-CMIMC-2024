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
        return self.task1(q, queryOutputs)
        # x1, y1 = self.pairs[0][0] # first 
        # x2, y2 = self.pairs[0][1] # second pair
        # if(x1 > x2):
        #     x1, x2 = x2, x1
        #     y1, y2 = y2, y1
        # plan = [[0] * self.n for i in range(self.n)]
        # #make 3 wide road from x1 to x2
        # for i in range(x1, x2 + 1):
        #     for j in range(max(y1 - 1,0), min(y1 + 2,16)):
        #         plan[i][j] = 1
        
        # #make 3 wide road from y1 to y2
        # if(y1 > y2):
        #     y1, y2 = y2, y1
        # for i in range(max(x2 - 1,0), min(x2 + 2,16)):
        #     for j in range(y1, y2 + 1):
        #         plan[i][j] = 1
            


        # return plan

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
        
