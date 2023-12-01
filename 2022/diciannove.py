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
        print(ore, clay, obsidian, geodude)

def getMust(blue):
    return (
        max([recipe[0] for recipe in blue]),
        blue[2][1],
        blue[3][2]
    )

sums = [1]
for i in range(2,maxMinute + 2):
    sums.append(i + sums[-1])

musts = {}
for b in blue:
    musts[str(b)] = getMust(b)

def canBuild(recipe, ores):
    # se posso costruire ogni robot allora devo farlo
    return not (False in [my >= ex for my, ex in zip(ores, recipe)])

def simulateDeque(blue) -> int:
    bfs = deque()
    bfs.append((0, (1,0,0,0), (0,0,0,0)))
    bar = tqdm(total= pow(4, maxMinute-14), leave=False, position=1)
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
            bar.update(1)
            if ores[-1] > best:
                best = ores[-1]
                #print(robots)
            continue

        # controllo se ho possibilita di battere il record
        if sums[maxMinute - minute - 1] + ores[-1] + (maxMinute - minute) * robots[-1] <= best:
            continue

        # robots = [0,0,0,0]
        # ore = [0,0,0,0]
        for type, recipe in enumerate(blue):
            # costruisco un robot solo se non ne ho gia abbastanza per costruire ogni robot
            # costruisco un robot non per geodi solo se non posso gia costruire un geodude a turno
            if canBuild(recipe, ores) and (type == 3 or robots[type] < musts[str(blue)][type]) and (type == 3 or robots[0] < blue[-1][0] or robots[2] < blue[-1][2]):
                newRobots = [r for r in robots]
                newRobots[type] += 1
                newOres = [old - cost + rob for old, cost, rob in zip(ores, recipe, robots)]

                bfs.append((minute + 1, newRobots, newOres))
        # se posso costruire tutti i robot non conviene skippare il turno
        if not canBuild(musts[str(blue)], ores):
            bfs.append((minute + 1, robots,[old + rob for old, rob in zip(ores, robots)]))
    bar.close()
    return best

quality = []
#dynamic = {}
for i, b in tqdm(enumerate(blue), total= len(blue)):
    #quality.append((i + 1)* simulate(b, 0, [1,0,0,0], [0,0,0,0]))
    #dynamic = {}
    quality.append(simulateDeque(b))
print(quality)
print(sum([ (i + 1) * qua for i, qua in enumerate(quality)]))

