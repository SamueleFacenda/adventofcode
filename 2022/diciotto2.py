from collections import deque

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

cubes: list['Point'] = []
with open('input', 'r') as f:
    for line in f:
        nums = [int(x) for x in line.split(',')]
        cubes.append(Point(nums[0], nums[1], nums[2]))

maxX = max([p.x for p in cubes])
maxY = max([p.y for p in cubes])
maxZ = max([p.z for p in cubes])
grid = [[[0 for _ in range(maxZ+2)] for e in range(maxY+2)] for j in range(maxX+2)]
# 0 is air
for p in cubes:
    grid[p.x][p.y][p.z] = 1 # is lava

out = 0

dfs = deque()
dfs.append(Point(0,0,0))
while len(dfs) > 0:
    p = dfs.pop()
    faces = [
        Point(p.x, p.y, p.z + 1),
        Point(p.x, p.y, p.z - 1),
        Point(p.x, p.y + 1, p.z),
        Point(p.x, p.y - 1, p.z),
        Point(p.x + 1, p.y, p.z),
        Point(p.x - 1, p.y, p.z),
    ]
    for f in faces:
        if f.y >= 0 and f.x >= 0 and f.z >= 0 and f.x < len(grid) and f.y < len(grid[0]) and f.z < len(grid[0][0]):
            if grid[f.x][f.y][f.z] == 0:
                grid[f.x][f.y][f.z] = 2
                dfs.append(f)


for p in cubes:
    faces = [
        Point(p.x, p.y, p.z + 1),
        Point(p.x, p.y, p.z - 1),
        Point(p.x, p.y + 1, p.z),
        Point(p.x, p.y - 1, p.z),
        Point(p.x + 1, p.y, p.z),
        Point(p.x - 1, p.y, p.z),
    ]
    for f in faces:
        if f.y < 0 or f.y > maxY or f.x < 0 or f.z < 0 or f.x > maxX or f.z > maxZ:
            out += 1
        elif grid[f.x][f.y][f.z] == 2:# is water
            out += 1

print(out)