grid = []

with open('input', 'r') as f:
    for line in f.readlines():
        grid.append([int(x) for x in line.strip()])

x_len = len(grid[0])
y_len = len(grid)

grid_visible = [[False for x in range(x_len)] for y in range(y_len)]

for y in range(y_len):
    # for every row start from left
    max_h = -1
    for x in range(x_len):
        if grid[y][x] > max_h:
            max_h = grid[y][x]
            grid_visible[y][x] = True

    # for every row start from right
    max_h = -1
    for x in range(x_len-1, -1, -1):
        if grid[y][x] > max_h:
            max_h = grid[y][x]
            grid_visible[y][x] = True

for x in range(x_len):
    # for every col start from top
    max_h = -1
    for y in range(y_len):
        if grid[y][x] > max_h:
            max_h = grid[y][x]
            grid_visible[y][x] = True

    # for every col start from bottom
    max_h = -1
    for y in range(y_len-1, -1, -1):
        if grid[y][x] > max_h:
            max_h = grid[y][x]
            grid_visible[y][x] = True

# count visible
visible = 0
for line in grid_visible:
    for tree in line:
        if tree:
            visible += 1



print(visible)
