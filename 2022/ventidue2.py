
map = []
path = None
with open('input2', 'r') as f:
    for line in f:
        if '.' in line:
            map.append(line[:-1])#remove \n
        else:
            path = line.strip()

width = max([len(x) for x in map])
for i, line in enumerate(map):
    map[i] += ' ' * (width - len(line))

right = path.split('R')
path = []
for i, segment in enumerate(right):
    left = segment.split('L')
    for j, subseq in enumerate(left):
        if subseq != '':
            path.append(int(subseq))
        if j != len(left) - 1:
            path.append('L')
    if i != len(right) - 1:
        path.append('R')

y = 0
x = min(map[0].index('#'), map[0].index('.'))
facing = 0 # 0 destra, 1 sotto, 2 sinistra, 3 sopra
def password(face, x, y):
    return (y+1) * 1000 + (x+1) * 4 + face

def move(face, x, y):
    match face:
        case 0:
            return x+1, y
        case 1:
            return x, y+1
        case 2:
            return x-1, y
        case 3:
            return x, y-1

def isOut(x, y):
    return x < 0 or y < 0 or x >= len(map[0]) or y >= len(map)

def next(face, x, y):
    newX, newY = move(face, x, y)
    if isOut(newX, newY) or map[newY][newX] == ' ':
        newX, newY, char, newFace = pacman(face, x, y)
        #print(f'{x=}, {y=}, {newX=}, {newY=}, {face=}, {newFace=}, {char=}')
            
        if char == '#':
            return x, y, face
        elif char == '.':
            return newX, newY, newFace
        else:
            print('carattere strano: ', char)
    if map[newY][newX] == '#':
        return x, y, face
    return newX, newY, face

side = int(len(map[0]) / 3)
flatH = int(len(map) / side)
flatW = side * 3
filled = [[' ' for i in range(flatW)] for _ in range(flatH)]
for r in range(flatH):
    for c in range(flatW):
        filled[r][c] = '#' if '.' in map[r * side][c * side : c * side + side - 1] else ' '
for i in filled:
    print(''.join(i))

def pacman(direction, x, y):
 ##
 #
##
#
    colonna = int(x / side)
    riga = int(y / side)
    lato = 0
    match direction:
        case 0:
            lato = riga + 3
        case 1:
            lato = 9 - colonna
        case 2:
            lato = 13 - riga
        case 3:
            lato = colonna
    #print(lato)
    try:
        match lato:
            case 0:
                # 12
                return side, x+ side, map[x+side][side], 0
            case 1:
                # to 10
                return 0, x + side + side, map[x+side+side][0], 0 
            case 2:
                # to 9
                return x - side - side, len(map) - 1, map[-1][x-side-side], 3
            case 3:
                # 5
                return side + side - 1, side + side + side - y - 1, map[side+side+side-y-1][side+side-1], 2
            case 4:
                # 7
                return y + side, side - 1, map[side-1][y+side], 3
            case 5:
                # 3
                return  len(map[0]) - 1, side - y + side + side - 1,map[side+side+side-y-1][-1], 2
            case 6:
                # 8
                return y - side - side, side + side + side - 1, map[side+side+side-1][y-side-side], 3
            case 7:
                # 4
                return side + side - 1, x - side, map[x-side][side+side-1], 2
            case 8:
                # 6
                return side - 1, x + side + side, map[x+side+side][side-1], 2
            case 9:
                # 2
                return x + side + side, 0, map[0][x+side+side], 1
            case 10:
                # 1
                return y-side-side, 0, map[0][y-side-side], 1
            case 11:
                # 13
                return side, side + side + side - y - 1, map[side+side+side-y-1][side], 0
            case 12:
                # 0
                return y - side, side  + side, map[side+side][y-side], 1
            case 13:
                # 11
                return 0, side + side + side - y - 1, map[side+side+side-y-1][0], 0
            case _:
                print(lato, riga, colonna, direction)
    except IndexError:
        print(lato, riga, colonna, direction)

trace = []
for i, movement in enumerate(path):
    if type(movement) == str:
        facing = (facing + (1 if movement == 'R' else 3)) % 4
    else:
        for _ in range(movement):
            x, y, facing = next(facing, x, y)
            trace.append((x, y, facing))


for x, y, facing in trace:
    map[y] = map[y][:x] + (['>', 'v', '<', '^'][facing]) + map[y][x+1:]
#for i in map:
#    print(''.join(i))

# 160144 high
# 172178 sbagliato
# 110340 giusto dovrebbe essere
# forse 110342
# 110342
# 110342
print(password(facing, x, y))