from tqdm import tqdm, trange

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f' Point: {self.x=}, {self.y=} '
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

def getNearOutsidePoints(sens, beac):
    dist = manDis(sens,beac)
    out = []
    for i, y in enumerate(range(sens.y - dist - 1, sens.y + 1)):
        out.append(Point(y, sens.x - i))
        out.append(Point(y, sens.x + i))
    for i, y in enumerate(range(sens.y + dist, sens.y, -1)):
        out.append(Point(y, sens.x - i))
        out.append(Point(y, sens.x + i))
    return out

def isInRange(sens, beac, check):
    return manDis(sens, check) <= manDis(sens, beac)

maxPos = 4000000

for sens, beac in tqdm(sens_beac):
    for p in tqdm(getNearOutsidePoints(sens, beac), leave=False, position=1):
        if p.x >= 0 and p.y >= 0 and p.x <= maxPos and p.y <= maxPos:
            outside = 0
            while outside < len(sens_beac) and not isInRange(sens_beac[outside][0], sens_beac[outside][1], p):
                outside += 1
            if outside == len(sens_beac):
                print(p)
                print(p.x * maxPos + p.y)
                exit()

