import random
import numpy as np
import math
import time

CalculateIterations = 60000
SimulationIterations = 50
moveChances = np.array([0.25,0.25,0.25,0.25])

directions = [(1,0),(0,1),(-1,0),(0,-1)]

def _CalculateInfiniteGeometricSeries(a_1, a_2, a_3 = None):
    r = a_2 / a_1
    if not a_3 is None:
        if a_3 / a_2 != r:
            raise ValueError("Not geometric sum :(")
    s = a_1 / (1 - r)
    return s



def _NeighbourExists(grid : list[list[bool]], x, y):
    for dir in directions:
        nx = x+dir[0]
        ny = y+dir[1]
        if nx >= len(grid) or nx < 0 or ny >= len(grid[0]) or ny < 0:
            continue
        if grid[nx][ny]:
            return True
    return False

def _CalculateSquare(grid : list[list[bool]]):
    x = random.randint(0, len(grid)-1)
    y = random.randint(0, len(grid[0])-1)
    while (grid[x][y]):
        x = random.randint(0, len(grid)-1)
        y = random.randint(0, len(grid[0])-1)

    while True:
        if _NeighbourExists(grid, x, y):
            return x, y
        while True:
            dir = random.randint(0, 3)
            nx = x+directions[dir][0]
            ny = y+directions[dir][1]
            if nx < len(grid) and nx >= 0 and ny < len(grid[0]) and ny >= 0:
                break
        x = nx
        y = ny

def Simulate(grid : list[list[bool]]):
    for i in range(SimulationIterations):
        x, y = _CalculateSquare(grid)
        grid[x][y] = True
    return grid

def CalculateProbabilities(grid : list[list[bool]]):
    sizeX = len(grid)
    sizeY = len(grid[0])

    Probs = np.zeros((sizeX, sizeY))

    for i in range(CalculateIterations):
        Probs[_CalculateSquare(grid)] += 1

    Probs /= Probs.sum()

    return Probs

# not good
def MarkovChainProbabilitesToMaxProb(grid : list[list[bool]], maxProb = 0.5, stepsPerCalc = 10):
    res = None
    maxEmptySpotValue = 1
    npgrid = np.array(grid)
    markedCount = npgrid.sum()
    posCount = npgrid.shape[0] * npgrid.shape[1]
    nonMarkedCount = posCount - markedCount
    startProb = 1 / nonMarkedCount
    maxProb = maxProb * startProb
    neighbours = np.array(npgrid)
    for x in range(npgrid.shape[0]):
        for y in range(npgrid.shape[1]):
            if _NeighbourExists(grid, x, y):
                neighbours[x,y] = True
    neighbours = np.logical_not(neighbours)
    while (maxEmptySpotValue > maxProb):
        res = MarkovChainProbabilites(grid, stepsPerCalc, res)
        temp = res * neighbours
        maxEmptySpotValue = temp.max()
    return res


def MarkovChainProbabilites(grid : list[list[bool]], steps : int, newProb = None):
    sizeX = len(grid)
    sizeY = len(grid[0])

    npgrid = np.array(grid)

    markedCount = npgrid.sum()
    posCount = sizeX * sizeY
    nonMarkedCount = posCount - markedCount
    startProb = 1 / nonMarkedCount

    neighbours = np.array(npgrid)

    if newProb is None:
        newProb = np.zeros((sizeX, sizeY))

    for x in range(sizeX):
        for y in range(sizeY):
            if npgrid[x,y] == False:
                newProb[x,y] = startProb
            if _NeighbourExists(grid, x, y):
                neighbours[x,y] = True

    for j in range(steps):
        oldProb = newProb
        newProb = np.zeros((sizeX, sizeY))
        for x in range(sizeX):
            for y in range(sizeY):
                if neighbours[x,y]:
                    newProb[x,y] += oldProb[x,y]
                    continue
                distribution = np.array(moveChances)
                for i in range(len(directions)):
                    dir = directions[i]
                    nx = x+dir[0]
                    ny = y+dir[1]
                    if nx >= len(grid) or nx < 0 or ny >= len(grid[0]) or ny < 0:
                        distribution[i] = 0
                        distribution /= distribution.sum()
                        continue
                for i in range(len(directions)):
                    dir = directions[i]
                    nx = x+dir[0]
                    ny = y+dir[1]
                    if nx >= len(grid) or nx < 0 or ny >= len(grid[0]) or ny < 0:
                        continue
                    newProb[nx,ny] += oldProb[x,y] * distribution[i]
    return newProb


class VoidHole:
    def __init__(self, startPos, grid : np.ndarray[bool], keepFields = False):
        self.posDict : dict[tuple[int,int],dict[tuple[int,int], float]] = {}
        self.frontier = {startPos}
        self.grid = grid
        self.keepFields = keepFields

    def _AddToOrCreateKey(self, key1, key2, value):
        if key2 in self.posDict[key1].keys():
            self.posDict[key1][key2] += value
        else:
            self.posDict[key1][key2] = value

    def _InBounds(self, position):
        if position[0] >= self.grid.shape[0] or position[0] < 0 or \
           position[1] >= self.grid.shape[1] or position[1] < 0:
            return False
        return True

    def _HasFilledNeighbour(self, x, y):
        for dir in directions:
            temp = (dir[0]+x,dir[1]+y)
            if not self._InBounds(temp):
                continue
            if self.grid[temp]:
                return True
        return False

    def CaculateAll(self):
        while len(self.frontier) != 0:
            self.calculateNext()

    def calculateNext(self, pos = None):
        # allows custom orders for debugging purposes
        if pos is None:
            pos = self.frontier.pop()
        else:
            self.frontier.remove(pos)

        # Add new positions to frontier for future could do this later but doesn't matter
        self.posDict[pos] = {}
        for dir in directions:
            temp = (dir[0]+pos[0],dir[1]+pos[1])
            if not self._InBounds(temp):
                continue
            if self._HasFilledNeighbour(*temp):
                continue
            if self.grid[temp]:
                raise Exception("Shouldn't happen, neighbour can't get picked")
            if not temp in self.posDict.keys():
                self.frontier.add(temp)

        # hardest and weirdest part, should work, calculates how much the pos will give off. Sounds weird and counterintuitiv because it is, but the chance above 100 is justified by removing the chance to return from all neighbouring fields
        # good luck understanding this, took me 1 entire day
        totalAmount = 4
        voidedAmount = 0
        totalBacktrackChance = 0
        for dir in directions:
            temp = (dir[0]+pos[0],dir[1]+pos[1])
            if not self._InBounds(temp):
                totalAmount -= 1
                continue
            if temp in self.posDict.keys():
                voidedAmount += 1
                totalBacktrackChance += self.posDict[temp][pos]
                #thisDirChance = _CalculateInfiniteGeometricSeries(1/4,1/4*backtrackChance*1/4)
        value = 1 / totalAmount # chance to go in any direction
        escapingChance = _CalculateInfiniteGeometricSeries(1, value * totalBacktrackChance)
        chanceGoingToNew = escapingChance * value

        # Apply the Chance to everything and sum
        for dir in directions:
            temp = (dir[0]+pos[0],dir[1]+pos[1])
            if not self._InBounds(temp):
                continue
            if not temp in self.posDict.keys():
                self._AddToOrCreateKey(pos, temp, chanceGoingToNew)
            else:
                voidField = self.posDict[temp]
                for key in voidField.keys():
                    if key == pos:
                        continue
                    self._AddToOrCreateKey(pos, key, chanceGoingToNew * self.posDict[temp][key])

        # remove unnecessary fields
        self.keepFields
        #TODO

        # Update every other Field
        for key in self.posDict.keys():
            if key == pos:
                continue
            field = self.posDict[key]
            value = field[pos]
            field.pop(pos) # remove for less loop time
            for key2 in self.posDict[pos].keys():
                self._AddToOrCreateKey(key, key2, value * self.posDict[pos][key2])
        return

class VoidHoleAggregate:
    def __init__(self, grid : np.ndarray[bool], cacheSize=5) -> None:
        self.grid = grid
        self.holes : list[VoidHole] = []
        self.closestFilled : np.ndarray[int] = None
        self._UpdateClosest()

    def _UpdateClosest(self):
        self.closestFilled = Deepseek_compute_manhattan_distance(self.grid)

    def _InBounds(self, position):
        if position[0] >= self.grid.shape[0] or position[0] < 0 or \
           position[1] >= self.grid.shape[1] or position[1] < 0:
            return False
        return True

    def _get_neighbours(self, pos):
        neighbours = []
        for dir in directions:
            temp = (dir[0]+pos[0],dir[1]+pos[1])
            if not self._InBounds(temp):
                continue
            neighbours.append(temp)
        return neighbours

    def _get_neighboured_grid(self):
        neighboured = np.array(self.grid)
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                for pos in self._get_neighbours((x,y)):
                    if self.grid[pos]:
                        neighboured[x,y] = True
                        break
        return neighboured

    def CalculateAllHoles(self):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.closestFilled[x, y] <= 1:
                    continue
                ignore = False
                for hole in self.holes:
                    if (x, y) in hole.posDict.keys():
                        ignore = True
                        break
                if ignore:
                    continue
                newHole = VoidHole((x,y), self.grid)
                newHole.CaculateAll()
                self.holes.append(newHole)

    def CalculateAllProbabilites(self):
        amount = 0
        probs = np.zeros(self.grid.shape, dtype=np.float32)
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x,y]:
                    continue
                amount += 1
                if self.closestFilled[x, y] <= 1:
                    probs[x,y] += 1
                    continue
                targetHole = None
                for hole in self.holes:
                    if (x,y) in hole.posDict.keys():
                        targetHole = hole
                        break
                if targetHole is None:
                    raise Exception("No Hole containing this position")
                for key in targetHole.posDict[(x,y)].keys():
                    probs[key] += targetHole.posDict[(x,y)][key]
        probs /= amount
        return probs





def VoidHoleProbabilities(grid : list[list[bool]]):
    grid = np.array(grid)
    aggr = VoidHoleAggregate(grid)
    aggr.CalculateAllHoles()
    probs = aggr.CalculateAllProbabilites()
    return probs


# def chatGPT_manhattan_distance_transform(bool_array):
#     rows, cols = bool_array.shape
#     # Initialize distances with a large number
#     dist = np.full((rows, cols), np.inf)
#     q = deque()

#     # Start from all True cells (distance 0)
#     for i in range(rows):
#         for j in range(cols):
#             if bool_array[i, j]:
#                 dist[i, j] = 0
#                 q.append((i, j))
    
#     # Directions for Manhattan neighbors (up, down, left, right)
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
#     # Multi-source BFS
#     while q:
#         i, j = q.popleft()
#         for di, dj in directions:
#             ni, nj = i + di, j + dj
#             if 0 <= ni < rows and 0 <= nj < cols:
#                 if dist[ni, nj] > dist[i, j] + 1:
#                     dist[ni, nj] = dist[i, j] + 1
#                     q.append((ni, nj))
    
#     return dist.astype(int)

def Deepseek_compute_manhattan_distance(arr):
    rows, cols = arr.shape
    max_distance = rows + cols  # A value larger than the maximum possible Manhattan distance
    dist = np.where(arr, 0, max_distance).astype(int)
    
    # First pass: top to bottom, left to right
    for i in range(rows):
        for j in range(cols):
            if i > 0:
                dist[i, j] = min(dist[i, j], dist[i-1, j] + 1)
            if j > 0:
                dist[i, j] = min(dist[i, j], dist[i, j-1] + 1)
    
    # Second pass: bottom to top, right to left
    for i in range(rows-1, -1, -1):
        for j in range(cols-1, -1, -1):
            if i < rows - 1:
                dist[i, j] = min(dist[i, j], dist[i+1, j] + 1)
            if j < cols - 1:
                dist[i, j] = min(dist[i, j], dist[i, j+1] + 1)
    
    return dist

def VoidGuess():
    grid = np.zeros((4, 4), dtype=np.float32)

    grid[1,1] = 1

    positions = [(1,1),(2,1),(2,2)]#,(1,2)]
    for i in range(1000):
        for pos in positions:
            value = grid[*pos]
            value *= 1/4
            grid[*pos] = 0
            for dir in directions:
                temp = (dir[0]+pos[0],dir[1]+pos[1])
                grid[*temp] += value
    return grid




if __name__ == "__main__":
    grid = np.zeros((300, 300), dtype=np.bool_)
    grid[15,15] = True
    grid[15,14] = True
    grid[15,16] = True
    grid[16,16] = True

    # currentTime = time.time()
    # chatGPT = chatGPT_manhattan_distance_transform(grid)
    # chatGPT_Time = time.time() - currentTime
    # print("ChatGPT", chatGPT_Time * 1000, "milliseconds")
    #Deepseek
    currentTime = time.time()
    Deepseek = Deepseek_compute_manhattan_distance(grid)
    Deepseek_Time = time.time() - currentTime
    print("Deepseek", Deepseek_Time * 1000, "milliseconds")

    # for x in range(grid.shape[0]):
    #     for y in range(grid.shape[1]):
    #         if chatGPT[x,y] != Deepseek[x,y]:
    #             raise Exception("Not same RESULTS!!!! WHYYY")

    input()

    exit()

    currentTime = time.time()
    res = VoidHoleProbabilities(grid)
    #res2 = VoidGuess()
    print(res[13:18,13:18])
    #print(res2)
    print(time.time()-currentTime)

    # currentTime = time.time()
    # res = CalculateProbabilities(grid)
    # print(res[13:17,13:17])
    # print(time.time()-currentTime)

    currentTime = time.time()
    res = MarkovChainProbabilites(grid, 2000, res)
    print(res[13:18,13:18])
    print(time.time()-currentTime)

    #res = MarkovChainProbabilitesToMaxProb(grid)
    #print(res)