from collections import deque

markel_len = 14

with open('input','r') as f:
    lines = f.readlines()
    tmp = deque()
    for i, car in enumerate(lines[0]):
        if i < markel_len - 1:
            tmp.append(car)
            continue
        
        if i != markel_len - 1:
            tmp.popleft()
        tmp.append(car)
        check = set()
        for j in tmp:
            check.add(j)
        if len(check) == markel_len:
            print(i+1)
            break

        


