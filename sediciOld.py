
valve = {}
valveArray = []
class Valve:
    def __init__(self, power, near, name):
        self.name = name
        self.power = power
        self.near = near
    def __str__(self):
        return f'{self.name=}, {self.power=}, near:{str(self.near)}'
    

class State:
    def __init__(self):
        self.pos = 'AA'
        self.minute = 1
        self.opened = 0
        self.valveStatus = {}
        self.initDict()
        self.totalPower = 0
        self.releasedPower = 0

    def initDict(self):
        for valv in valveArray:
            self.valveStatus[valv.name] = False

    def move(self, to):
        self.next()
        self.pos = to
        return self

    def next(self):
        self.minute += 1
        self.releasedPower += self.totalPower
        return self

    def open(self):
        self.next()
        if not self.valveStatus[self.pos]:
            self.valveStatus[self.pos] = True
            self.totalPower += valve[self.pos].power
            self.opened += 1
        return self

    def copy(self):
        out = State()
        out.pos = self.pos
        out.minute = self.minute
        out.opened = self.opened
        out.totalPower = self.totalPower
        out.releasedPower = out.releasedPower
        for valv in valveArray:
            out.valveStatus[valv.name] = self.valveStatus[valv.name]
        return out
    
    def __hash__(self):
        stringa = self.pos + str(self.minute) + '|' + str(self.valveStatus)
        return hash(stringa)
        
with open('input', 'r') as f:
    for line in f:
        name = line.split(' ')[1]
        power = int(line.split('=')[1].split(';')[0])
        near = list(map(lambda x: x.strip(), line.split('to valve')[1][1:].split(',')))
        valv = Valve(power, near, name)
        valve[name] = valv
        valveArray.append(valv)


start = State()
maxMinute = 30
usefulValves = 0
dynamic = {}

for valv in valveArray:
    if valv.power > 0:
        usefulValves += 1

def bestMove(state: State):
    if state.minute <= 22:
        print(str(state.minute) + ('#' * state.minute))

    if state.minute == maxMinute + 1:
        return state.releasedPower

    if state in dynamic:
        return dynamic[state]

    if state.opened >= usefulValves:
        print("yea")
        best = bestMove(state.copy().next())
        dynamic[state] = best
        return best
    else:
        best = 0
        for near in valve[state.pos].near:
            tmp = state.copy()
            tmp.move(near)
            tmp = bestMove(tmp)
            if tmp > best:
                best = tmp
        if valve[state.pos].power > 0:
            tmp = bestMove(state.copy().open())
            if tmp > best:
                best = tmp
        dynamic[state] = best
        return best
    
bestt = bestMove(start)

print(bestt)