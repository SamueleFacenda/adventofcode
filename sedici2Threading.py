from collections import deque
from tqdm import tqdm
from threading import Thread, Lock

valve: dict[str, 'Valve'] = {}
valveArray: list['Valve'] = []
class Valve:
    def __init__(self, power, near, name):
        self.name = name
        self.power = power
        self.near = near
        self.routes: dict[str, 'Path'] = {}
    def __str__(self):
        return f'{self.name=}, {self.power=}, near:{str(self.near)}, routes({len(self.routes)}): {Path.strDict(self.routes)}'

class Path:
    def __init__(self, source: Valve, weight: int):
        self.source = source
        self.weight = weight
    def __str__(self):
        return f'from {self.source.name}, {self.weight}'
    def strDict(dict: dict['Path']):
        return ' '.join([str(fro) + '->' +str(path) for fro, path in dict.items()])

class Update:
    def __init__(self, node: Valve, path: Path, to: str):
        self.node = node
        self.path = path
        self.to = to
        
with open('input', 'r') as f:
    for line in f:
        name = line.split(' ')[1]
        power = int(line.split('=')[1].split(';')[0])
        near = list(map(lambda x: x.strip(), line.split('to valve')[1][1:].split(',')))
        valv = Valve(power, near, name)
        valve[name] = valv
        valveArray.append(valv)

# find the shortest from every node with a power to every other one
# bellam-ford alghoritm(distance vector)
# o almeno penso, ho le mie tabelle di routing su un nodo, se le aggiorno lo dico ai vicini

# trovo i nodi da raggiungere
primaryNodes = []
for valv in valveArray:
    if valv.power > 0:
        primaryNodes.append(valv)

# inizializzo le tabelle
for valv in valveArray:
    for primary in primaryNodes:
        valv.routes[primary.name] = Path(None, float('inf'))

que: deque['Update'] = deque()
for prim in primaryNodes:
    que.append(Update(prim, Path(prim, 0), prim.name))

# main cicle
while len(que) > 0:
    current = que.popleft()
    path = current.path
    node = current.node
    if path.weight < current.node.routes[current.to].weight:
        node.routes[current.to] = path
        for near in node.near:
            que.append(Update(valve[near], Path(node, path.weight + 1), current.to))


#print('\n'.join([str(v) for v in valveArray]))


maxMinute = 26
usefulValves = len(primaryNodes)
dynamic = {}

allPoss = {}

def bestMove(pos, minute, visited, power, mem):
    if mem:
        global allPoss
        if not str(sorted(visited)) in allPoss:
            allPoss[str(sorted(visited))] = (visited, power)
        else:
            if allPoss[str(sorted(visited))][1] < power:
                allPoss[str(sorted(visited))] = (visited, power)
    # dynamic programming
    stringa = str(pos) + str(minute) + str(visited)
    if stringa in dynamic:
        return dynamic[stringa]

    # ho aperto tutte le valvole, tiro dritto
    if len(visited) >= usefulValves :
        dynamic[stringa] = power
        return power
    else:
        out = []
        # è aperta, mi muovo da qualche altra parte
        for key, value in valve[pos].routes.items():
            if (key not in visited) and value.weight + minute + 1 <= maxMinute:
                out.append(bestMove(key, minute + value.weight + 1, visited + [key], power + (valve[key].power * (maxMinute - minute - value.weight - 1)), mem))
        out = max(out) if len(out) > 0 else power
        dynamic[stringa] = out
        return out

bestOut = 0
lock = Lock()
def funcWrapper(visited, power):
    out = bestMove('AA', 0, visited, 0, False) + power
    global bestOut
    with lock:
        if out > bestOut:
            bestOut = out

bestMove('AA', 0, [], 0, True)
threads = []
for key, value in tqdm(allPoss.items()):
    threads.append(Thread(target=funcWrapper, args=(value[0], value[1])))
    threads[-1].start()

for thread in tqdm(threads):
    thread.join()

print(bestOut)
