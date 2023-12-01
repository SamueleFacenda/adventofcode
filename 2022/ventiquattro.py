from collections import deque

grid = []

with open('input') as f:
    for line in f:
        grid.append([ x for x in line.strip()])

# replace grid <>v^ with 0 1 2 3
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '<':
            grid[i][j] = 3
        elif grid[i][j] == '>':
            grid[i][j] = 1
        elif grid[i][j] == 'v':
            grid[i][j] = 2
        elif grid[i][j] == '^':
            grid[i][j] = 0
        elif grid[i][j] == '.':
            grid[i][j] = -1
        elif grid[i][j] == '#':
            grid[i][j] = -2

def move(x, y, dir):
    if dir == 0:
        return x, y - 1
    elif dir == 1:
        return x + 1, y
    elif dir == 2:
        return x, y + 1
    elif dir == 3:
        return x - 1, y
    else:
        print('error in move', dir)


minute = [grid]
print('\n'.join([','.join([str(y).zfill(2) for y in x]) for x  in grid]))

# 0 su, 1 destra, 2 giu, 3 sinistra
def getMinute(min):
    if min >= len(minute) - 1:
        for _ in range(min - len(minute) + 1):
            # update the grid
            newGrid = []
            for i in range(len(minute[-1])):
                newGrid.append([])
                for j in range(len(minute[-1][i])):
                    if type(minute[-1][i][j]) == list or minute[-1][i][j] >= 0:
                        newGrid[i].append(-1)
                    else:
                        newGrid[i].append(minute[-1][i][j])
            
            # ho copiato la griglia, adesso aggiorno i tornadi
            for i in range(len(minute[-1])):
                for j in range(len(minute[-1][i])):
                    if not type(minute[-1][i][j]) == list and minute[-1][i][j] < 0:
                        continue
                    lista = []
                    if type(minute[-1][i][j]) == list:
                        lista = minute[-1][i][j]
                    else:
                        lista = [minute[-1][i][j]]
                    for k in lista:
                        x, y = move(j, i, k)
                        if newGrid[y][x] == -1:
                            newGrid[y][x] = k
                        elif newGrid[y][x] == -2:
                            if x == len(minute[-1][0]) - 1:
                                x = 1
                            elif x == 0:
                                x = len(minute[-1][0]) - 2
                            elif y == len(minute[-1]) - 1:
                                y = 1
                            elif y == 0:
                                y = len(minute[-1]) - 2
                            # se e' negativo parte dalla fine
                            if newGrid[y][x] == -1:
                                newGrid[y][x] = k
                            elif type(newGrid[y][x]) == list:
                                newGrid[y][x].append(k)
                            elif newGrid[y][x] >= 0:
                                newGrid[y][x] = [k, newGrid[y][x]]
                            else:
                                print('error in pacman')
                        elif type(newGrid[y][x]) == list:
                            newGrid[y][x].append(k)
                        elif newGrid[y][x] >= 0:
                            newGrid[y][x] = [k, newGrid[y][x]]
                        else:
                            print('error')
            minute.append(newGrid)
            #print('\n'.join([','.join([str(y).zfill(2) for y in x]) for x  in newGrid]))

def bestTIme(fro, to, startGrid):
    best = float('inf')
    global minute
    minute = [startGrid]

    dfs = deque()
    dfs.append((fro[0], fro[1], 0)) # x, y, min
    dyn = {}
    while len(dfs) > 0:
        x, y, min = dfs.pop()
        if str((x, y, min)) in dyn:
            continue
        dyn[str((x, y, min))] = True
        if min >= best:
            continue
        if (x, y) == to:
            best = min
            print('found', best)
            continue
        
        # move next turn
        getMinute(min + 1)
        
        for i in range(4):
            x1, y1 = move(x, y, i)
            if x1 < 0 or x1 >= len(grid[0]) or y1 < 0 or y1 >= len(grid):
                continue

            if type(minute[min+1][y1][x1]) != list and minute[min+1][y1][x1] == -1:
                dfs.appendleft((x1, y1, min + 1))

        # wait
        if type(minute[min+1][y][x]) != list and minute[min+1][y][x] == -1:
            dfs.appendleft((x, y, min + 1))
    return best

uno = bestTIme((1, 0), (len(grid[0]) - 2, len(grid) - 1), grid)
due = bestTIme((len(grid[0]) - 2, len(grid) - 1), (1, 0), minute[-2])
tre = bestTIme((1, 0), (len(grid[0]) - 2, len(grid) - 1), minute[-2])
print(uno + due + tre)