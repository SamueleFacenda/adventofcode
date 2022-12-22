
def priority(letter):
    num = ord(letter)
    if num >= 65 and num <= 90:
        return num - 64 + 26
    elif num >= 97 and num <= 122:
        return num - 96


total = 0
with open('input', 'r') as f:
    group = 0
    back = [{}, {}, {}]
    for line in f:
        if group == 3:
            group = 0
            print(back[2].keys())
            total += priority(list(back[2].keys())[0])
            back = [{}, {}, {}]
        group += 1

        line = line.strip()
        for letter in line:
            if group == 1:
                back[0][letter] = True
            elif group == 2:
                if letter in back[0]:
                    back[1][letter] = True
            elif group == 3:
                if letter in back[1]:
                    back[2][letter] = True


    total += priority(list(back[2].keys())[0])

print(total)

