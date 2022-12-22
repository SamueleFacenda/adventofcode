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


monkeys = {} # is operation, (num) / (num1, num2, operation)

with open('input', 'r') as f:
    for line in f:
        name, altro = line.split(':')
        altro = altro.strip().split(' ')
        if len(altro) == 1:
            monkeys[name] = (False,int(altro[0]))
        else:
            monkeys[name] = (True, altro[1], altro[0], altro[2])

def solve(name):
    if name == 'humn':
        return 'humn'
    tmp = monkeys[name]
    if tmp[0]:
        uno = solve(tmp[2])
        due = solve(tmp[3])
        if uno != 'humn' and due != 'humn' and type(uno) is not tuple and type(due) is not tuple:
            return operation(tmp[1], uno, due)
        else:
            return (tmp[1], uno, due)
    else:
        return tmp[1]

left, right = solve(monkeys['root'][2]), solve(monkeys['root'][3])
print(left)
print(right)
if type(right) is tuple:
    left, right = right, left

while True:
    if 'humn' in left:
        print(str(right) + '=' + str(left))
        break
    op = left[0]
    match op:
        case '+':
            if type(left[1]) is tuple:
                right -= left[2]
                left = left[1]
            else:
                right -= left[1]
                left = left[2]
        case '-':
            if type(left[1]) is tuple:
                right += left[2]
                left = left[1]
            else:
                right -= left[1]
                right = -right
                left = left[2]
        case '*':
            if type(left[1]) is tuple:
                right /= left[2]
                left = left[1]
            else:
                right /= left[1]
                left = left[2]
        case '/':
            if type(left[1]) is tuple:
                right *= left[2]
                left = left[1]
            else:
                right = left[1] / right
                left = left[2]
