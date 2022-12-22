from tqdm import trange

def operation(oper, num1, num2):
    match oper:
        case '+':
            return num1 + num2
        case '-':
            return num1 - num2
        case '*':
            return num1 * num2
        case '/':
            return num1 / num2
        case _:
            print(oper)
subscribers: dict[str, list['Monkey']] = {}
monkeys: dict[str, 'Monkey']= {}
class Monkey:
    def __init__(self, name):
        self.name = name
    def subscribe(self, name):
        if not name in subscribers:
            subscribers[name] = []
        subscribers[name].append(self)
    def hearYell(self, name, value):
        print('UnsupportedOperationException', self.name)
        raise RuntimeError()

class OperationMonkey(Monkey):
    def __init__(self, name, operation, sub1, sub2):
        super().__init__(name)
        self.operation = operation
        self.subscribe(sub1)
        self.subscribe(sub2)
        self.state: list[tuple[bool, int]] = [(False, 0), (False, 0)]
        self.subbed: dict[str, int] = {sub1: 0, sub2: 1}

    def hearYell(self, name, value):
        self.state[self.subbed[name]] = (True, value)
        if not False in [x[0] for x in self.state]:
            if self.name == 'root':
                #print('root ', str(result))
                #return -1
                global root
                root = self.state[0][1] == self.state[1][1]
            else:
                result = operation(self.operation, self.state[0][1], self.state[1][1])
                for monkey in subscribers[self.name]:
                    monkey.hearYell(self.name, result)

numberMonkeys: list[tuple[str, int]] = []

with open('input', 'r') as f:
    for line in f:
        name, altro = line.split(':')
        altro = altro.strip().split(' ')
        if len(altro) == 1:
            numberMonkeys.append((name, int(altro[0])))
        else:
            monkeys[name] = OperationMonkey(name, altro[1], altro[0], altro[2])
root = None
for i in trange(1000000000000000000):
    root = False

    for num in numberMonkeys:
        for subbed in subscribers[num[0]]:
            subbed.hearYell(num[0], num[1] if num[0] != 'humn' else i)

    if root:
        print(i)
        break
        
