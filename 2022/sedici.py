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


#print('\n'.join([str(v) for v in valveArray]))


class State:
    def __init__(self):
        self.pos: str = 'AA'
        self.minute: int = 0
        self.opened: int = 0
        self.valveStatus: dict[bool] = {}
        self.initDict()
        self.totalPower: int = 0
        self.releasedPower: int = 0
        self.trace = ''

    def initDict(self):
        for valv in valveArray:
            self.valveStatus[valv.name] = False

    def move(self, to):
        weight = valve[self.pos].routes[to].weight
        self.minute += weight
        self.releasedPower += weight * self.totalPower
        self.pos = to
        self.trace += to
        return self

    def next(self):
        self.minute += 1
        self.releasedPower += self.totalPower
        return self

    def open(self):
        self.next()
        if not self.valveStatus[self.pos]:
            if valve[self.pos].power == 0:
                print("apro una valvola difettosa")
            self.valveStatus[self.pos] = True
            self.totalPower += valve[self.pos].power
            self.opened += 1
        else:
            print("error voglio aprire una già aperta")
        return self

    def copy(self):
        out = State()
        out.pos = self.pos
        out.minute = self.minute
        out.opened = self.opened
        out.totalPower = self.totalPower
        out.releasedPower = self.releasedPower
        out.trace = self.trace
        for valv in valveArray:
            out.valveStatus[valv.name] = self.valveStatus[valv.name]
        return out
    
    def __hash__(self):
        stringa = self.pos + str(self.minute) + '|' + str(self.valveStatus)
        return hash(stringa)

start = State()
maxMinute = 30
usefulValves = len(primaryNodes)
dynamic = {}
#i = 0

def bestMove(state: State):

    #initial = state.copy()

    # uscita dalla ricorsione, ho raggiunto i minuti previsti
    if state.minute >= maxMinute - 1:
        state.next()
        #bar.update(1)
        return state.releasedPower

    # dynamic programming
    #if state in dynamic:
    #    bar.update(pow(len(primaryNodes)-1, maxMinute - state.minute))
    #    return dynamic[state]

    # ho aperto tutte le valvole, tiro dritto
    if state.opened >= usefulValves :
        best = state.releasedPower + state.totalPower * (maxMinute - state.minute)
        #dynamic[initial] = best
        #bar.update(1)
        #best = bestMove(state.next())
        return best
    else:
        best = 0
        if state.valveStatus[state.pos] or valve[state.pos].power == 0:
            # è aperta, mi muovo da qualche altra parte
            for key, value in valve[state.pos].routes.items():
                if (not state.valveStatus[key]) and value.weight + state.minute <= maxMinute - 1:
                    tmp = state.copy()
                    tmp.move(key)
                        
                    tmp = bestMove(tmp)
                    if tmp == lastBest:
                        print(key)
                        if state.pos == 'AA':
                            print('-')
                    if tmp > best:
                        best = tmp
        else:
            best = bestMove(state.open())
        #dynamic[initial] = best
        if best == 0:
            #print('nada')
            # questo non dovrebbe succedere
            # non potevo raggiungere nessun posto
            best = state.releasedPower + state.totalPower * (maxMinute - state.minute)
            #best = bestMove(state.next())
            #bar.update(1)

        return best


#print(usefulValves)
#print(str(valve[start.pos]))
#total = pow(usefulValves, usefulValves) * usefulValves
#print(total)
#bar = tqdm(total = total)

lastBest = -1
lastBest = bestMove(start)
bestt = bestMove(State())
#bar.close()

#print(bestMove(State().move('DD').open().move('BB').open().move('JJ').open().move('HH').open().move('EE').open().move('CC').open()))

print(bestt)
# best: DD BB JJ HH EE CC