import random


class Planner:
    def setup(self, pairs, bd):
        self.n = 16
        self.pairs = pairs
        self.bd = bd
        self.yeetProbability = 0.07  # probability of removing a road
        self.bestPlan = [[1] * self.n for i in range(self.n)]
        self.sentPlan = []
        return

    def task1(self, q, queryOutputs):  # p = 5, bd = 0.25
        l = len(queryOutputs)
        if l > 0 and queryOutputs[l - 1]:
            self.bestPlan = self.sentPlan
        n = self.n
        newPlan = [[1] * n for i in range(n)]

        # take the most recent successful plan
        # remove each road with small probability
        for i in range(n):
            for j in range(n):
                newPlan[i][j] = self.bestPlan[i][j]
                if newPlan[i][j] == 1:
                    rando = random.uniform(0, 1)
                    if rando < self.yeetProbability:
                        newPlan[i][j] = 0

        self.sentPlan = newPlan
        return self.sentPlan

    def task2(self, q, queryOutputs): # p = 5, bd = 0.1
        return self.task1(q, queryOutputs)

    def task3(self, q, queryOutputs): # p = 1, bd = 0.25
        return self.task1(q, queryOutputs)

    def task4(self, q, queryOutputs): # p = 1, bd = 0.1
        x1, y1 = self.pairs[0][0] # first pair
        x2, y2 = self.pairs[0][1] # second pair
        if(x1 > x2):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        plan = [[0] * self.n for i in range(self.n)]
        #make 3 wide road from x1 to x2
        for i in range(x1, x2 + 1):
            for j in range(max(y1 - 1,0), min(y1 + 2,16)):
                plan[i][j] = 1
        
        #make 3 wide road from y1 to y2
        if(y1 > y2):
            y1, y2 = y2, y1
        for i in range(max(x2 - 1,0), min(x2 + 2,16)):
            for j in range(y1, y2 + 1):
                plan[i][j] = 1
            


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
        
