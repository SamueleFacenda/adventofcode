x = 1 # sprite position
pos_ctl = 0
width = 40
heigth = 6
screen = ['.' for _ in range(width * heigth)]

def print_screen():
    for i in range(heigth):
        print(''.join(screen[i*width:(i+1)*width]))

def cycle_next():
    global pos_ctl
    if abs((pos_ctl) % width  - x) <= 1:
        screen[pos_ctl] = '#' 
    pos_ctl += 1

    
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

print_screen()