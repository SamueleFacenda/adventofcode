grid = []

with open('input', 'r') as f:
    for line in f.readlines():
        grid.append([int(x) for x in line.strip()])

x_len = len(grid[0])
y_len = len(grid)

def computate_scenic_score(y, x):
    left = 0
    right = 0
    top = 0
    bottom = 0
    start_h = grid[y][x]

    # left
    for i in range(x - 1, -1, -1):
        left += 1
        if grid[y][i] >= start_h:
            break
    if left == 0:
        return 0

    # right
    i = x + 1
    for i in range(x + 1, x_len):
        right += 1
        if grid[y][i] >= start_h:
            break
    if right == 0:
        return 0

    # top
    for i in range(y - 1, -1, -1):
        top += 1
        if grid[i][x] >= start_h:
            break
    if top == 0:
        return 0
    
    # bottom
    for i in range(y + 1, y_len):
        bottom += 1
        if grid[i][x] >= start_h:
            break
    if bottom == 0:
        return 0
        

    return left * right * top * bottom

max_score = 0
for y in range(y_len):
    for x in range(x_len):
        score = computate_scenic_score(y, x)
        if score > max_score:
            max_score = score

print(max_score)