from tqdm import trange, tqdm
from collections import deque
# 0 ore
# 1 clay 
# 2 obsidian
# 3  geodude

blue: list[tuple[tuple, tuple, tuple, tuple]]= []
maxMinute = 24

with open('input', 'r') as f:
    for line in f:
        line = line.split(':')[1]
        part = line.split('.')
        ore = (int(part[0].split(' ')[-2]),0,0,0)
        spl = part[3].split(' ')
        geodude = (int(spl[5]), 0, int(spl[8]),0)
        spl = part[2].split(' ')
        obsidian = (int(spl[5]), int(spl[8]),0,0)
        clay = (int(part[1].split(' ')[-2]),0,0,0)
        blue.append((ore, clay, obsidian, geodude))

def getMust(blue):
    return (
        max([recipe[0] for recipe in blue]),
        blue[2][1],
        blue[3][2]
    )

sums = [1]
for i in range(2,maxMinute + 2):
    sums.append(i + sums[-1])

print(sums)
musts = {}
for b in blue:
    musts[str(b)] = getMust(b)

def canBuild(recipe, ores):
    # se posso costruire ogni robot allora devo farlo
    return not False in [my >= ex for my, ex in zip(ores, recipe)]

def simulateDeque(blue) -> int:
    bfs = deque()
    bfs.append((0, (1,0,0,0), (0,0,0,0)))
    best = 0
    dynamic = {}
    while len(bfs) > 0:
        minute, robots, ores = bfs.pop()
        stringa = str(minute) + str(robots) + str(ores)
        if stringa in dynamic:
            continue
        else:
            dynamic[stringa] = True
        if minute == maxMinute:
            if ores[-1] > best:
                best = ores[-1]
                print(robots)
            continue

        # controllo se ho possibilita di battere il record
        if sums[maxMinute - minute - 1] + ores[-1] + (maxMinute - minute) * robots[-1] <= best:
            continue

        # robots = [0,0,0,0]
        # ore = [0,0,0,0]
        ores = [old + rob for old, rob in zip(ores, robots)]
        for type, recipe in enumerate(blue):
            if canBuild(recipe, ores):
                newRobots = [r for r in robots]
                newRobots[type] += 1
                newOres = [old - cost for old, cost in zip(ores, recipe)]

                bfs.append((minute + 1, newRobots, newOres))
        if not canBuild(musts[str(blue)], ores):
            bfs.append((minute + 1, robots, ores))

    return best



def simulate(blue, min, robots, ores) -> int:
    stringa = str(min) + str(robots) + str(ores)
    if stringa in dynamic:
        return dynamic[stringa]

    if min == maxMinute:
        return ores[-1]
    # robots = [0,0,0,0]
    # ore = [0,0,0,0]
    ores = [old + rob for old, rob in zip(ores, robots)]
    best = 0
    for type, recipe in enumerate(blue):
        if canBuild(recipe, ores):
            newRobots = [r for r in robots]
            newRobots[type] += 1
            newOres = [o for o in ores]
            newOres[0] -= recipe[0]
            if type == 2:
                newOres[1] -= recipe[1]
            elif type == 3:
                newOres[2] -= recipe[1]

            tmp = simulate(blue, min+1, newRobots, newOres)
            best = max(tmp, best)
    if not canBuild(musts[str(blue)], ores):
        tmp = simulate(blue, min + 1, robots, ores)
        best = max(tmp, best)

    dynamic[stringa] = best
    return best

quality = []
#dynamic = {}
for i, b in tqdm(enumerate(blue), total= len(blue)):
    #quality.append((i + 1)* simulate(b, 0, [1,0,0,0], [0,0,0,0]))
    #dynamic = {}
    quality.append(simulateDeque(b))

print(quality)
print(sum([ (i + 1) * qua for i, qua in enumerate(quality)]))

