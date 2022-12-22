
scans = []

high_y = 0
high_x = 0
low_x = float('inf')

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f'Point {self.x=} {self.y=}'

with open('input') as f:
    for line in f:
        moves = line.split(' -> ')
        scans.append([])
        for move in moves:
            spl = move.split(',')
            scans[-1].append(Point(int(spl[0]), int(spl[1])))
            if int(spl[0]) > high_x:
                high_x = int(spl[0])
            if int(spl[1]) > high_y:
                high_y = int(spl[1])
            if int(spl[0]) < low_x:
                low_x = int(spl[0])


# create a grid of the right size
grid = []
for i in range(high_y + 4):
    grid.append([])
    for j in range(high_x + 2):
        grid[-1].append('.')

def writeOrizontal(left, right):
    for x in range(left.x, right.x + 1):
        grid[left.y][x] = '#'
def writeVertical(top, bottom):
    for y in range(bottom.y, top.y + 1):
        grid[y][top.x] = '#'

def writeLine(fromm, to):
    if fromm.x == to.x:
        if fromm.y > to.y:
            writeVertical(fromm, to)
        else:
            writeVertical(to, fromm)
    elif fromm.y == to.y:
        if fromm.x > to.x:
            writeOrizontal(to, fromm)
        else:
            writeOrizontal(fromm, to)
    else:
        print(f'error: {fromm=} {to=}')

# write all the lines on the grid
for path in scans:
    # sliding window
    for i in range(len(path) - 1):
        writeLine(path[i], path[i + 1])

def printGrid():
    for line in grid:
        print(''.join(line[low_x: high_x + 1]))

printGrid()


def newSand():
    pos = Point(500, 0)
    # return True if stopped, False if finished away
    while True:
        if pos.y > high_y + 2:
            return False

        # move down
        if grid[pos.y + 1][pos.x] == '.':
            pos.y += 1
        # down left
        elif grid[pos.y + 1][pos.x - 1] == '.':
            pos.y += 1
            pos.x -= 1
        # down right
        elif grid[pos.y + 1][pos.x + 1] == '.':
            pos.y += 1
            pos.x += 1
        else:
            # stopped
            grid[pos.y][pos.x] = 'o'
            return True

i = 0
while newSand():
    i += 1
print(i)

