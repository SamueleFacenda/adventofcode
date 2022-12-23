elfi = []
mappa = []

with open('input', 'r') as f:
    for y, line in enumerate(f):
        mappa.append([])
        for x, cell in enumerate(line):
            if cell == '\n':
                continue
            mappa[y].append(cell)
            if cell == '#':
                elfi.append((x, y))

nRounds = 1000
for i in range(len(mappa)):
    mappa[i] = ['.'] * nRounds + mappa[i] + ['.'] * nRounds
width = len(mappa[1])

for _ in range(nRounds):
    mappa.insert(0, ['.'] * width)
    mappa.append(['.'] * width)

def printMap():
    print('\n'.join([''.join(line) for line in mappa]))

#printMap()

def canMove(x, y, direction):
    match direction:
        case 0:
            return mappa[y-1][x-1] != '#' and mappa[y-1][x] != '#' and mappa[y-1][x+1] != '#'
        case 1:
            return mappa[y-1][x+1] != '#' and mappa[y][x+1] != '#' and mappa[y+1][x+1] != '#'
        case 2:
            return mappa[y+1][x-1] != '#' and mappa[y+1][x] != '#' and mappa[y+1][x+1] != '#'
        case 3:
            return mappa[y-1][x-1] != '#' and mappa[y][x-1] != '#' and mappa[y+1][x-1] != '#'

def needToMove(x, y):
    return mappa[y-1][x-1] == '#' or mappa[y-1][x] == '#' or mappa[y-1][x+1] == '#' or mappa[y+1][x-1] == '#' or mappa[y+1][x] == '#' or mappa[y+1][x+1] == '#' or mappa[y][x-1] == '#' or mappa[y][x+1] == '#'

def move(x, y, direction):
    match direction:
        case 0:
            return x, y-1
        case 1:
            return x+1, y
        case 2:
            return x, y+1
        case 3:
            return x-1, y
for i in range(len(elfi)):
    elfi[i] = (elfi[i][0] + nRounds, elfi[i][1] + nRounds)
card = (0, 2, 3, 1)
def infinity():
    i = 0
    while True:
        yield i
        i += 1

for dir in infinity():
    moves = []
    # trovo tutti i movimenti che gli elfi vogliono fare
    for num, elfo in enumerate(elfi):
        if not needToMove(*elfo):
            continue
            # passo all'elfo successivo
        x, y = elfo
        for i in range(4):
            if canMove(x, y, card[(dir + i)%4]):
                moves.append((num, card[(dir + i)%4], move(x, y, card[(dir + i)%4])))
                break
    nextCells = [x[2] for x in moves]
    doMove = [True for _ in moves]
    #tolgo tutti i movimenti che vogliono essere fatti da piu' elfi
    for i, cell in enumerate(nextCells):
        if nextCells.count(cell) > 1:
            doMove[i] = False

    for i, movement in enumerate(moves):
        if doMove[i]:
            mappa[elfi[movement[0]][1]][elfi[movement[0]][0]] = '.'
            elfi[movement[0]] = movement[2]
            mappa[movement[2][1]][movement[2][0]] = '#'

    if not (True in doMove):
        print(dir+1)
        break
    #print(moves)
    #printMap()


maxX = max([x[0] for x in elfi])
minX = min([x[0] for x in elfi])
maxY = max([x[1] for x in elfi])
minY = min([x[1] for x in elfi])
notElf = 0
for y in range(minY, maxY+1):
    for x in range(minX, maxX+1):
        if mappa[y][x] != '#':
            notElf += 1

#print(notElf)