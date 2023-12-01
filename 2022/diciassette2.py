from math import lcm
import time
from tqdm import tqdm
width = 7
numOfRocks = 1000000000000
nShapes = 5

def infinity():
    index = 0
    while True:
        yield index
        index += 1

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @staticmethod
    def ix(dir):
        match dir:
            case 1:
                return 1
            case 3:
                return -1
            case (0|2):
                return 0
    @staticmethod
    def yp(dir):
        match dir:
            case 0:
                return 1
            case 2:
                return -1
            case (1|3):
                return 0
    def move(self, dir):
        return Point(self.x + Point.ix(dir), self.y + Point.yp(dir))
    def __str__(self):
        return f'{self.x=}, {self.y=}'

class Shape:
    def __init__(self, arr):
        self.arr: list['Point'] = arr
    def move(self, dir):
        return Shape([p.move(dir) for p in self.arr])
    def moveUp(self, dist):
        return Shape([Point(p.x, p.y + dist) for p in self.arr])
    def edges(self):
        edges = [-float('inf'), -float('inf'), float('inf'), float('inf')]
        for p in self.arr:
            if p.y > edges[0]:
                edges[0] = p.y
            if p.x > edges[1]:
                edges[1] = p.x
            if p.y < edges[2]:
                edges[2] = p.y
            if p.x < edges[3]:
                edges[3] = p.x
        return edges

    

class Chamber:
    def __init__(self, moveSeq):
        self.grid: list[list[str]] = [['.'] * width]
        self.heigth = -1
        self.movements = moveSeq
        self.index = 0
        self.jetIndex = 0
        self.shapes: list['Shape'] = [
            Shape([Point(2,0), Point(3,0), Point(4,0), Point(5,0)]),
            Shape([Point(2,1), Point(3,0), Point(3,1), Point(3,2), Point(4,1)]),
            Shape([Point(2,0), Point(3,0), Point(4,0), Point(4,1), Point(4,2)]),
            Shape([Point(2,0), Point(2,1), Point(2,2), Point(2,3)]),
            Shape([Point(2,0), Point(3,0), Point(3,1), Point(2,1)])            
        ]
    def fallShape(self):
        shape = self.shapes[self.index % len(self.shapes)]
        self.index += 1
        shape = shape.moveUp(self.getHeigth() + 4)
        up = shape.edges()[0]
        if up + 1 > len(self.grid):
            offset = up -len(self.grid) + 1
            self.addLines(offset)
        #print(f'{up=}, {self.heigth=}, {len(self.grid)=}')
        self.heigth = up

        for i in infinity():
            dir = None
            if i % 2 == 0:
                dir = self.movements[self.jetIndex % len(self.movements)]
                self.jetIndex += 1
            else:
                dir = 2
            niu = shape.move(dir)
            if self.canShape(niu):
                shape = niu
                if dir == 2:
                    self.heigth -= 1
            else:
                if dir == 2:
                    self.printShape(shape)
                    return


    def addLines(self, num):
        for _ in range(num):
            self.grid.append(['.'] * width)

    def canShape(self, s: Shape):
        for p in s.arr:
            if not self.canPoint(p):
                return False
        return True

    def getHeigth(self):
        for i in range(len(self.grid) - 1, -1, -1):
            if '#' in self.grid[i]:
                return i
        return -1
    def canPoint(self, p: Point):
        if p.x >= len(self.grid[0]) or p.x < 0:
            return False
        if p.y < 0:
            return False
        try:
            return self.grid[p.y][p.x] != '#'
        except:
            self.printGrid()
            print(str(p))
            print('index:' +str(self.index % len(self.shapes)))
            raise Exception()
    def printShape(self, s:Shape, clear=False):
        for p in s.arr:
            self.grid[p.y][p.x] = '.' if clear else '#'
    def printGrid(self, shape=None):
        if shape is not None:
            self.printShape(shape)
        for i in range(len(self.grid)-1, -1, -1):
            print(''.join(self.grid[i]))
        print()
        if shape is not None:
            self.printShape(shape, clear=True)
    def getTail(self, lenght=20):
        i = len(self.grid) - 1
        found = 0
        out = []
        while found < lenght:
            if '#' in self.grid[i]:
                out.append(self.grid[i])
                found += 1
            i -= 1
        return str(out)

moves = []
with open('input', 'r')as f:
    for c in f.readline():
        match c:
            case '<':
                moves.append(3)
            case '>':
                moves.append(1)
chamber = Chamber(moves)

cycle = lcm(len(moves), nShapes)
print(cycle)
for _ in range(cycle):
    chamber.fallShape()

tails = {}

completeCycleHeight = None
cycleLenght = None
completedCycle = 1
lastTail = chamber.getTail()
tails[lastTail] = (chamber.getHeigth(), completedCycle)

firstPart = time.time()
animate = time.time()
while True:
    for _ in range(cycle):
        chamber.fallShape()
    completedCycle += 1
    niuEnd = chamber.getTail()
    if niuEnd in tails:
        startH, startC = tails[niuEnd]
        cycleLenght = completedCycle - startC
        completeCycleHeight = chamber.getHeigth() - startH
        break
    tails[niuEnd] = (chamber.getHeigth(), completedCycle)
    print(len(tails))

print('trovato ciclo al tentativo n.'+ str(completedCycle)) 
firstPart = time.time() - firstPart
print(f'{firstPart=}')
out = chamber.getHeigth()
beforeLastStep = out
newCycle = cycleLenght * cycle
skip = int((numOfRocks - completedCycle * cycle) / newCycle)
out += skip * completeCycleHeight
# 1570928990643 too low
second = time.time()
tq = tqdm(total=firstPart)
for _ in range(cycle * (skip * cycleLenght + completedCycle), numOfRocks):
    chamber.fallShape()
    tq.update(time.time() - second)
    second = time.time()
out += chamber.getHeigth() - beforeLastStep + 1
tq.close()
print(out)
print('1514285714288')
