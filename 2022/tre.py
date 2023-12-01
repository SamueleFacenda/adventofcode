
def priority(letter):
    num = ord(letter)
    if num >= 65 and num <= 90:
        return num - 64 + 26
    elif num >= 97 and num <= 122:
        return num - 96


total = 0
with open('input', 'r') as f:
    for line in f:
        back = {}
        line = line.strip()
        lenght = len(line)
        for i, letter in enumerate(line):
            if i < lenght / 2:
                back[letter] = True
            else:
                if letter in back:
                    total += priority(letter)
                    break


print(total)

