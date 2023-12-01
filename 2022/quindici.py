from tqdm import tqdm
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
sens_beac = []
with open('input', 'r') as f:
    for line in f:
        splitted = line.split(',')
        sensorX = splitted[0].split('=')[1]
        sensorY = splitted[1].split('=')[1].split(':')[0]
        beaconX = splitted[1].split('=')[2]
        beaconY = splitted[2].split('=')[1]
        sensor = Point(int(sensorX), int(sensorY))
        beacon = Point(int(beaconX), int(beaconY))
        sens_beac.append((sensor, beacon))

# get Manhattan distance
def manDis(uno, due):
    return abs(uno.x - due.x) + abs(uno.y - due.y)

# find the min x, max x, min y, min x
minX = min(map(lambda c: min(c[0].x, c[1].x) - manDis(c[0], c[1]), sens_beac))
minY = min(map(lambda c: min(c[0].y, c[1].y) - manDis(c[0], c[1]), sens_beac))
maxX = max(map(lambda c: min(c[0].x, c[1].x) + manDis(c[0], c[1]), sens_beac))
maxY = max(map(lambda c: min(c[0].y, c[1].y) + manDis(c[0], c[1]), sens_beac))

class Grid:
    def __init__(self, minX, minY, maxX, maxY):
        self.width = maxX - minX
        self.height = maxY - minY + 1
        self.baseX = minX + 1
        self.baseY = minY
        self.grid = [['.'] * self.width  for _ in range(self.height)]
    def __str__(self):
        return ''.join([(''.join(row)) + '\n' for row in self.grid])
    def _setCell(self, x, y, value):
        if self._getCell(x, y) == '.' or self._getCell(x, y) == '#':
            self.grid[y - self.baseY][x - self.baseX] = value
    def _getCell(self, x, y):
        return self.grid[y - self.baseY][x - self.baseX]
    def addCouple(self, sens, beacon):
        dist = manDis(sens, beacon)
        # parte alta del rombo
        for i, y in enumerate(range(sens.y - dist, sens.y + 1)):
            for x in range(sens.x - i, sens.x + i + 1):
                self._setCell(x, y, '#')
        for i, y in enumerate(range(sens.y + dist, sens.y, -1)):
            for x in range(sens.x - i, sens.x + i + 1):
                self._setCell(x, y, '#')
        self._setCell(sens.x, sens.y, 'S')
        self._setCell(beacon.x, beacon.y, 'B')
    def countHashtag(self, y):
        return self.grid[y - self.baseY].count('#')

#grid = Grid(minX, minY, maxX, maxY)
#for sens, beacon in tqdm(sens_beac):
#    grid.addCouple(sens, beacon)
#print(grid)
pos = 2000000
#pos = 10
#print(grid.countHashtag(pos))
line = ['.'] * (maxX - minX )
for sens, beacon in sens_beac:
    dist = manDis(sens, beacon)
    vertDist = abs(sens.y - pos)
    if vertDist <= dist:
        orizLength = dist - vertDist
        for i in range(sens.x - orizLength, sens.x + orizLength + 1):
            line[i - minX] = '#'
for sens, beacon in sens_beac:
    if sens.y == pos:
        line[sens.x - minX] = 'S'
    if beacon.y == pos:
        line[beacon.x - minX] = 'B'
print(line.count('#'))

