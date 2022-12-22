from collections import deque

crates = []
i=0
with open('input', 'r') as f:

    first = True
    moves = False
    for line in f:
        if first:
            first = False
            crates = [deque() for _ in range(int(len(line)/4))]

        if len(line.strip()) == 0:
            moves = True
            print(crates)
            continue

        if not moves:
            for i, c in enumerate(line):
                if (i%4) == 1:
                    if ord(c) < 65 and c != ' ':
                        break

                    if c != ' ':
                        crates[int(i/4)].appendleft(c)
        else:
            _, num, _, da, _, to= line.split(' ')
            
            for _ in range(int(num)):
                crates[int(to)-1].append(crates[int(da)-1].pop())


out = ''
print(crates)
for crate in crates:
    if len(crate) > 0:
        out += crate.pop()
    else:
        out += ' '


print(out)




