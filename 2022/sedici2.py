from collections import deque
from tqdm import tqdm

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

solutions = []
maxTime = 26

def findSolution(node: Valve, score, time, visited: list[str]):
    global solutions
    solutions.append((score, visited))
    values = []
    for key, dist in node.routes.items():
        if name not in visited and key != node.name and time + dist.weight < maxTime - 1:
            values.append(findSolution(valve[key], score + valve[key].power * (maxTime - time), time + dist.weight, visited + [key]))
    return max(values) if len(values) > 0 else score

print(findSolution(valve['AA'], 0, 0, []))