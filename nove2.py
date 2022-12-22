import time
tail_pos = {}
goto = {
    'U' : lambda p: Point(p.x, p.y + 1),
    'D' : lambda p: Point(p.x, p.y - 1),
    'L' : lambda p: Point(p.x - 1, p.y),
    'R' : lambda p: Point(p.x + 1, p.y),
}
n_knot = 10

class Point:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

def is_already_right(head, tail):
    if head.x == tail.x and head.y == tail.y:
        return True
    if head.x == tail.x:
        return abs(head.y - tail.y) == 1
    if head.y == tail.y:
        return abs(head.x - tail.x) == 1
    # check diagonal
    return abs(head.x - tail.x) == 1 and abs(head.y - tail.y) == 1

def adjust_tail(head, tail):
    if is_already_right(head, tail):
        return tail
    
    if head.x == tail.x:
        if head.y > tail.y:
            return Point(tail.x, tail.y + 1)
        else:
            return Point(tail.x, tail.y - 1)
    if head.y == tail.y:
        if head.x > tail.x:
            return Point(tail.x + 1, tail.y)
        else:
            return Point(tail.x - 1, tail.y)

    # diagonal move to same row/column
    if abs(head.x - tail.x) == 1:
        # move to same column
        if head.y > tail.y:
            return Point(head.x, tail.y + 1)
        else:
            return Point(head.x, tail.y - 1)
    if abs(head.y - tail.y) == 1:
        # move to same row
        if head.x > tail.x:
            return Point(tail.x + 1, head.y)
        else:
            return Point(tail.x - 1, head.y)

    # diagonal move to diagonal
    if abs(head.x - tail.x) == 2 and abs(head.y - tail.y) == 2:
        if head.x > tail.x:
            if head.y > tail.y:
                return Point(tail.x + 1, tail.y + 1)
            else:
                return Point(tail.x + 1, tail.y - 1)
        else:
            if head.y > tail.y:
                return Point(tail.x - 1, tail.y + 1)
            else:
                return Point(tail.x - 1, tail.y - 1)
    print('error')
    print_pos()
    


total = 0
pos = [Point() for _ in range(n_knot)]
def print_pos():
    len = 25
    # create a grid
    grid = [['.' for _ in range(len)] for _ in range(len)]
    rndx = pos[0].x
    rndy = pos[0].y
    for i, p in enumerate(pos):
        if p is None:
            print(f'pos {i} is None')
            continue
        grid[p.y - rndx + int(len/2)][p.x - rndy + int(len/2)] = str(i)

    for row in grid:
        print(''.join(row))

debug = False

with open('input', 'r') as f:
    for line in f.readlines():
        dir, length = line.strip().split()
        length = int(length)
        for _ in range(length):
            pos[0] = goto[dir](pos[0])
            for i in range(1, n_knot):
                try:
                    pos[i] = adjust_tail(pos[i - 1], pos[i])
                except:
                    print('error')
                    print_pos()
                    exit(1)

                if debug:
                    print_pos()
                    time.sleep(0.5)


            if not str(pos[-1]) in tail_pos:
                total += 1
                tail_pos[str(pos[-1])] = True

print(total)