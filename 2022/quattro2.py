
total = 0

with open('input', 'r') as f:
    for line in f:
        line = line.strip()
        pa1, pa2 = line.split(',')
        pa1 = pa1.split('-')
        pa2 = pa2.split('-')

        if int(pa1[0]) >= int(pa2[0]) and int(pa1[0]) <= int(pa2[1]):
            total += 1
        elif int(pa1[1]) >= int(pa2[0]) and int(pa1[1]) <= int(pa2[1]):
            total += 1
        elif int(pa2[0]) >= int(pa1[0]) and int(pa2[0]) <= int(pa1[1]):
            total += 1
        elif int(pa2[1]) >= int(pa1[0]) and int(pa2[1]) <= int(pa1[1]):
            total += 1

print(total)