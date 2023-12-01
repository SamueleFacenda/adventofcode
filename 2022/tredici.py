
couples = []
#read input

def parseElement(element):

    if element[0] == '[':
        # è una lista
        element = element[1:-1]

        #split by comma, skipping embedded lists
        elements = []
        current = ''
        inList = 0
        for c in element:
            if c == '[':
                inList += 1
            if c == ']':
                inList -= 1
            if c == ',' and inList == 0:
                elements.append(current)
                current = ''
            else:
                current += c
        if len(current) > 0:
            elements.append(current)

        elements = [parseElement(e) for e in elements]
        return elements
    else:
        return int(element)

def parseLine(line):
    if line[0] != '[':
        print('error')
        return
    return parseElement(line)

    

with open('input') as f:
    index = 0
    inCoupleIndex = 0
    for line in f:
        line = line.strip()
        if line == '':
            index += 1
            inCoupleIndex = 0
            continue
        parsed = parseLine(line)
        if inCoupleIndex == 0:
            couples.append([parsed])
        else:
            couples[index].append(parsed)
        inCoupleIndex += 1

def isOrderRight(left, right):
    # return 0 if are ordered
    # return 1 if continue
    # return 2 if are not ordered

    nLists = 0
    nLists += type(left) is list
    nLists += type(right) is list
    if nLists == 0:
        if left == right:
            return 1
        elif left < right:
            return 0
        else:
            return 2

    if nLists == 1:
        if type(left) is list:
            return isOrderRight(left, [right])
        else:
            return isOrderRight([left], right)

    if nLists == 2:
        for i in range(max(len(left), len(right))):
            if i >= len(left) and i < len(right):
                return 0
            if i < len(left) and i >= len(right):
                return 2
            
            cmp = isOrderRight(left[i], right[i])
            if cmp == 0:
                return 0
            if cmp == 2:
                return 2
            # if cmp == 1: continue
        return 1


    print(f'error, {left=}, {right=}')


total = 0
for i, couple in enumerate(couples):
    left = couple[0]
    right = couple[1]
    cmp = isOrderRight(left, right)
    if cmp == 0:
        print(f'{i+1} is right')
        total += i + 1
    elif cmp == 2:
        print(f'{i+1} is wrong')
    elif cmp == 1:
        print(f'{i+1} is ambiguous')
    else:
        print(f'error, {cmp=}')

print(total)
