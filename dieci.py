x = 1
cycle = 0
total = 0
def cycle_next():
    global cycle
    cycle += 1
    if (cycle-20) % 40 == 0 and cycle <= 220:
        global x
        global total
        total += x * cycle
        print(f'{x=}, {cycle=}, {cycle*x=}')

with open('input') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('noop'):
            to_add = int(line.split()[1])
            cycle_next()
            cycle_next()
            x += to_add
        else:
            cycle_next()

print(total)