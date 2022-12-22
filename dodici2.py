from collections import deque

map = []
bestStart = None
end = None
class Point:
    def __init__(self, height,  y=0, x=0):
        self.y = y
        self.x = x
        self.visited = False
        self.distance = 100000000000
        self.previous = None
        self.height = height
        self.queued = False
    def __str__(self):
        return f"Point(y={self.y}, x={self.x}, visited={self.visited}, distance={self.distance})"
    def move(y, x, direction):
        if direction == 0:
            return (y - 1, x)
        elif direction == 1:
            return (y, x + 1)
        elif direction == 2:
            return (y + 1, x)
        elif direction == 3:
            return (y, x - 1)
    def getInDir(self, dir):
        ny, nx = Point.move(self.y, self.x, dir)
        if ny < 0 or nx < 0 or ny >= len(map) or nx >= len(map[0]):
            return None
        return map[ny][nx]
    def convertCharToHeight(self):
        if self.height == 'S':
            return 0
        elif self.height == 'E':
            return 25
        else:
            return ord(self.height) - ord('a')
    def canDirectionHeight(fro, to):
        return fro.convertCharToHeight() >= to.convertCharToHeight() - 1
    def dijkstra(self):
        if self.visited:
            return
        if self.height == 'a':
            global bestStart
            if not bestStart or self.distance < bestStart.distance:
                bestStart = self
        self.visited = True
        for i in range(4):
            to = self.getInDir(i)
            if to is None:
                continue
            if to.visited:
                continue
            if not Point.canDirectionHeight(to, self):
                continue
            if self.distance + 1 < to.distance:
                to.distance = self.distance + 1
                to.previous = self
                dijkstraQueue.append(to)

    def printPath(self):
        if self.previous is None:
            print(self)
            return
        self.previous.printPath()
        print(self)

        

with open('input', 'r') as f:
    for y, line in enumerate(f):
        map.append([])
        for x, char in enumerate(line):
            if char == '\n':
                continue
            map[y].append(Point(char, y, x))
            if char == 'S':
                map[y][x] = Point('a', y, x)
            elif char == 'E':
                end = map[y][x]

# dijkstra's algorithm
dijkstraQueue = deque()
end.distance = 0
dijkstraQueue.append(end)

while len(dijkstraQueue) > 0:
    point = dijkstraQueue.popleft()
    point.dijkstra()

bestStart.printPath()

print(bestStart.distance)
