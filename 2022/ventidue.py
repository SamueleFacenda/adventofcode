
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

def pacman(direction, index):
    match direction:
        case 0:
            return row(index, True)
        case 1:
            return column(index, True)
        case 2:
            return row(index, False)
        case 3:
            return column(index, False)

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
        newX, newY, char = pacman(face, (newY if face in (0,2) else newX))
        if char == '#':
            return x, y
        elif char == '.':
            return newX, newY
    if map[newY][newX] == '#':
        return x, y
    return newX, newY

for movement in path:
    if type(movement) == str:
        facing = (facing + (1 if movement == 'R' else 3)) % 4
    else:
        for _ in range(movement):
            x, y = next(facing, x, y)


print(password(facing, x, y))