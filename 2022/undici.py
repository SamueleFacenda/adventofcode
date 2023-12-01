

class Monkey:
    def __init__(self, items, doMultiply, operationNumber, testNumber, trueTest, falseTest) -> None:
        self.items = items
        self.doMultiply = doMultiply
        self.testNumber = testNumber
        self.trueTest = trueTest
        self.falseTest = falseTest
        self.operationNumber = operationNumber
        self.inspectCount = 0

    def inspect(self):
        # pop and inspect the first item
        self.inspectCount += 1
        item = self.items.pop(0)
        if self.operationNumber == 'old':
            if self.doMultiply:
                item = item * item
            else:
                item = item + item
        else:
            if self.doMultiply:
                item = item * int(self.operationNumber)
            else:
                item = item + int(self.operationNumber)
        return int(item / 3)

    def inspectAndThrow(self):
        newValue = self.inspect()
        if newValue % self.testNumber == 0:
            monkeyTo = self.trueTest
        else:
            monkeyTo = self.falseTest
        return (newValue, monkeyTo)

    def __str__(self) -> str:
        return f"Monkey(items={self.items}, doMultiply={self.doMultiply}, operationNumber={self.operationNumber}, testNumber={self.testNumber}, trueTest={self.trueTest}, falseTest={self.falseTest})"

monkeys = []
with open('input') as f:
    tmpMonkeys = Monkey([], False, 0, 0, 0, 0)
    for line in f:
        if line.startswith('  Starting items'):
            tmpMonkeys.items = [int(x) for x in line.split(':')[1].split(',')]
        elif line.startswith('  Operation'):
            tmpMonkeys.doMultiply = '*' in line
            tmpMonkeys.operationNumber = line.split()[-1]
        elif line.startswith('  Test'):
            tmpMonkeys.testNumber = int(line.split()[-1])
        elif line.startswith('    If true'):
            tmpMonkeys.trueTest = int(line.split()[-1])
        elif line.startswith('    If false'):
            tmpMonkeys.falseTest = int(line.split()[-1])
        elif len(line.strip()) == 0:
            monkeys.append(tmpMonkeys)
            tmpMonkeys = Monkey([], False, 0, 0, 0, 0)
    monkeys.append(tmpMonkeys)

nRound = 20
for i in range(nRound):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            newValue, monkeyTo = monkey.inspectAndThrow()
            monkeys[monkeyTo].items.append(newValue)

#max inspect count and second max inspect count
sorted = sorted(monkeys, key=lambda x: x.inspectCount, reverse=True)
print(sorted[0].inspectCount)
print(sorted[1].inspectCount)
# multiply the two
print(sorted[0].inspectCount * sorted[1].inspectCount)