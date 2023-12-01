
map = []
path = None
with open('input', 'r') as f:
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

def row(line, start):
    x, char = first(map[line], start)
    return x, line, char

def column(col, start):
    word = ''.join([line[col] for line in map])
    y, char = first(word, start)
    return col, y, char

def first(word, start):
    for i, char in enumerate(word if start else word[::-1]):
        if char != ' ':
            return (i if start else len(word) - i - 1), char

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
        newX, newY, char = pacman(face, x, y)
        if char == '#':
            return x, y
        elif char == '.':
            return newX, newY
    if map[newY][newX] == '#':
        return x, y
    return newX, newY

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
    riga = int(x / side)
    colonna = int(y / side)
    lato = 0
    match direction:
        case 0:
            lato = riga
        case 1:
            lato = 9 - colonna
        case 2:
            lato = 13 - riga
        case 3:
            lato = colonna
    try:
        match lato:
            case 0:
                # 12
                return row(side + x, True)
            case 1:
                # to 10
                return 0, y + side + side, map[y+side+side][0] 
            case 2:
                # to 9
                return x - side - side, len(map) - 1, map[-1][x-side-side]
            case 3:
                # 5
                return row(side + side+ side - y - 1, False)
            case 4:
                # 7
                return column(y + side, False)
            case 5:
                # 3
                return side - y + side + side - 1, len(map[0]) - 1, map[side+side+side-y][-1]
            case 6:
                # 8
                return column(y-side-side, False)
            case 7:
                # 4
                return row(x-side, False)
            case 8:
                # 6
                return row(x+side+side, False)
            case 9:
                # 2
                return x + side + side, 0, map[0][x+side+side]
            case 10:
                # 1
                return y-side-side, 0, map[0][y-side-side]
            case 11:
                # 13
                return row(side + side + side - y - 1, True)
            case 12:
                # 0
                return column(y - side, True)
            case 13:
                # 11
                return 0, side + side + side - y - 1, map[side+side+side-y-1][0]
            case _:
                print(lato, riga, colonna, direction)
    except IndexError:
        print(lato, riga, colonna, direction)


for movement in path:
    if type(movement) == str:
        facing = (facing + (1 if movement == 'R' else 3)) % 4
    else:
        for _ in range(movement):
            x, y = next(facing, x, y)


print(password(facing, x, y))