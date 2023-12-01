
snafu = {
    '2': 2,
    '0': 0,
    '1': 1,
    '-': -1,
    '=': -2, 
}

# reverse snafu dict
snafuRev = {v: k for k, v in snafu.items()}

def fromSNAFU(string):
    return sum([snafu[x] * pow(5, i) for i, x in enumerate(string[::-1])])

def toSNAFU(number):
    string = ''
    while number > 0:
        cifra = number % 5
        if cifra <= 2:
            string += snafuRev[cifra]
        else:
            number += 5
            string += snafuRev[cifra - 5]
        number //= 5
    return string[::-1]

somma = 0
with open('input') as f:
    for line in f:
        somma += fromSNAFU(line.strip())
        #print(fromSNAFU(line.strip()))

print(somma)
print(toSNAFU(somma))