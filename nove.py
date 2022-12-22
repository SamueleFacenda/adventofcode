
tail_pos = {}
goto = {
    'U' : lambda x, y: (x, y + 1),
    'D' : lambda x, y: (x, y - 1),
    'L' : lambda x, y: (x - 1, y),
    'R' : lambda x, y: (x + 1, y),
}

def is_already_right(h_x, h_y, t_x, t_y):
    if h_x == t_x and h_y == t_y:
        return True
    if h_x == t_x:
        return abs(h_y - t_y) == 1
    if h_y == t_y:
        return abs(h_x - t_x) == 1
    # check diagonal
    return abs(h_x - t_x) == 1 and abs(h_y - t_y) == 1

def adjust_tail(h_x, h_y, t_x, t_y):
    if is_already_right(h_x, h_y, t_x, t_y):
        return t_x, t_y
    
    if h_x == t_x:
        if h_y > t_y:
            return t_x, t_y + 1
        else:
            return t_x, t_y - 1
    if h_y == t_y:
        if h_x > t_x:
            return t_x + 1, t_y
        else:
            return t_x - 1, t_y

    # diagonal move to same row/column
    if abs(h_x - t_x) == 1:
        # move to same column
        if h_y > t_y:
            return h_x, t_y + 1
        else:
            return h_x, t_y - 1
    if abs(h_y - t_y) == 1:
        # move to same row
        if h_x > t_x:
            return t_x + 1, h_y
        else:
            return t_x - 1, h_y
    print('error')

def key(x, y):
    return f'{x},{y}'

total = 0
h_x = 0
h_y = 0
t_x = 0
t_y = 0
with open('input', 'r') as f:
    for line in f.readlines():
        dir, length = line.strip().split()
        length = int(length)
        for i in range(length):
            h_x, h_y = goto[dir](h_x, h_y)
            t_x, t_y = adjust_tail(h_x, h_y, t_x, t_y)
            if not key(t_x, t_y) in tail_pos:
                total += 1
                tail_pos[key(t_x, t_y)] = True

print(total)