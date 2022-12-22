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
class Action:
    def __init__(self, isOpening, to, len):
        self.len = len
        self.isOpening = isOpening
        self.to = to
    def copy(self):
        return Action(self.isOpening, self.to, self.len)
    def __str__(self):
        return str(self.len)+','+self.to+','+str(self.isOpening)

class State:
    def __init__(self):
        self.pos = ['AA', 'AA']
        self.doing: list['Action'] = [None, None]
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

    def next(self):
        self.minute += 1
        self.releasedPower += self.totalPower
        for i in range(len(self.doing)):
            if self.doing[i] is None:
                pass
                # non ci sono più cose da fare
            elif self.doing[i].isOpening:
                if not self.valveStatus[self.pos[i]]:
                    if valve[self.pos[i]].power == 0:
                        print("apro una valvola difettosa")
                    self.valveStatus[self.pos[i]] = True
                    self.totalPower += valve[self.pos[i]].power
                    self.opened += 1
                    self.doing[i] = None
                else:
                    print("error voglio aprire una già aperta")
            elif self.doing[i].to is not None:
                # si sta muovendo
                self.doing[i].len -= 1
                if self.doing[i].len == 0:
                    # sono arrivato
                    self.pos[i] = self.doing[i].to 
                    self.trace += self.pos[i]
                    self.doing[i] = None
            else:
                print("non so bene" + str(self.doing[i]))

        return self

    def copy(self):
        out = State()
        out.minute = self.minute
        out.opened = self.opened
        out.totalPower = self.totalPower
        out.releasedPower = self.releasedPower
        out.trace = self.trace
        out.doing = [x.copy() if x is not None else None for x in self.doing]
        out.pos = [x for x in self.pos]
        for valv in valveArray:
            out.valveStatus[valv.name] = self.valveStatus[valv.name]
        return out
    
    def __hash__(self):
        stringa = str(self.pos) + str(self.minute) + '|' + str(self.valveStatus) + '|' + '|'.join([str(x) for x in self.doing] )
        return hash(stringa)

start = State()
maxMinute = 26
usefulValves = len(primaryNodes)
dynamic = {}
#i = 0

def bestMove(state: State):
    if(len(state.trace)/2 == precision):
        bar.update(1)

    #initial = state.copy()

    # uscita dalla ricorsione, ho raggiunto i minuti previsti
    if state.minute >= maxMinute:
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
        # se ho già due azioni assegnate vado avanti

        best = 0
        if state.doing.count(None) == 0:
            best = bestMove(state.next())
        else:
            # faccio le azioni
            for i in range(len(state.pos)):
                if state.doing[i] is None:
                    if (state.pos[i] != state.pos[(i+1)%2] or state.doing[(i+1)%2] is None or not state.doing[(i+1)%2].isOpening) and not state.valveStatus[state.pos[i]] and valve[state.pos[i]].power != 0:
                        # l'altro o non sta facendo niente o comunque non sta aprendo questa valvola(o non sono sulla stessa valvola)
                        # e la valvola non è aperta
                        # e la valvola non vale zero
                        # la apro
                        tmp = state.copy()
                        tmp.doing[i] = Action(True, None, None)
                        best = bestMove(tmp)
                    else:
                        # è aperta, mi muovo da qualche altra parte
                        for key, value in valve[state.pos[i]].routes.items():
                            if not state.valveStatus[key] and value.weight + state.minute < maxMinute and (state.doing[(i+1)%2] is None or state.doing[(i+1)%2].to != key):
                                tmp = state.copy()
                                tmp.doing[i] = Action(False, key, value.weight)
                                tmp = bestMove(tmp)
                                if tmp > best:
                                    best = tmp

        #dynamic[initial] = best
        if best == 0:
            #print('nada')
            # questo non dovrebbe succedere
            # non potevo raggiungere nessun posto
            #best = state.releasedPower + state.totalPower * (maxMinute - state.minute)
            best = bestMove(state.next())
            #bar.update(1)

        return best


#print(usefulValves)
#print(str(valve[start.pos]))
#total = pow(usefulValves, usefulValves) * usefulValves
#print(total)
precision = 4
total = pow(usefulValves * 2, 4)
bar = tqdm(total = total)

lastBest = -1
lastBest = bestMove(start)
bestt = bestMove(State())
bar.close()

#print(bestMove(State().move('DD').open().move('BB').open().move('JJ').open().move('HH').open().move('EE').open().move('CC').open()))

print(bestt)
# best: DD BB JJ HH EE CC