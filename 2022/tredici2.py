from collections import deque

packets = []
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
        if len(line) == 0:
            continue
        packets.append(parseLine(line))
        

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


# merge sort

def mergeSort(arr):
    # uscita dalla ricorsione
    if len(arr) == 0:
        return deque()
    if len(arr) == 1:
        out = deque()
        out.append(arr[0])
        return out
        
    else:
        half = int(len(arr) / 2)
        #divide et impera
        uno, due = arr[0 : half], arr[half : len(arr)]
        # ricorsione
        uno = mergeSort(uno)
        due = mergeSort(due)
        # arrays are sorted, now I merge them(they are a deque now), in order
        output = deque()
        while len(uno) > 0 or len(due) > 0:
            if len(uno) == 0:
                output.append(due.popleft())
            elif len(due) == 0:
                output.append(uno.popleft())
            else:
                cmp = isOrderRight(uno[0], due[0])
                if cmp == 0:
                    output.append(uno.popleft())
                elif cmp == 2:
                    output.append(due.popleft())
                elif cmp == 1:
                    # they are equals
                    output.append(uno.popleft())
                    output.append(due.popleft())
                    
        return output
        

# aggiungo i delimitatori di pacchetto
delimitatorUno = [[2]]
delimitatorDue = [[6]]
packets.append(delimitatorUno)
packets.append(delimitatorDue)

packets = mergeSort(packets)


out = 1

# controllo la posizione dei delimitatori
for i, element in enumerate(packets):
    if element == delimitatorUno or element == delimitatorDue:
        print(element)
        print(i)
        out *= i + 1



print(f'{out=}')