from tqdm import tqdm, trange
nums = []
with open('input', 'r') as f:
    nums = [int(x) for x in f.readlines()]

class Node:
    def __init__(self, value, before=None, after=None):
        self.before: Node = before
        self.after: Node = after
        self.value = value
        self.dist = None
    
    def forward(self):
        oldAfter = self.after
        oldAfter.before = self.before
        self.after = oldAfter.after
        oldAfter.after = self
        self.before = oldAfter
        oldAfter.before.after = oldAfter
        self.after.before = self
    
    def backwards(self):
        oldBefore = self.before
        oldBefore.after = self.after
        self.before = oldBefore.before
        oldBefore.before = self
        self.after = oldBefore
        oldBefore.after.before = oldBefore
        self.before.after = self

    def move(self,value):
        if value > 0:
            for _ in range(value):
                self.forward()
        else:
            for _ in range(-value):
                self.backwards()

    def __str__(self):
        return f'{self.value=}, before={self.before.value}, after={self.after.value}'

key = 811589153
nums = [Node(x) for x in nums]
for num in nums:
    num.value = num.value * key
    if num.value > 0:
        num.dist = num.value % (len(nums) - 1)
    elif num.value < 0:
        num.dist = -1 * ((-1 * num.value) % (len(nums) -1))
    else:
        num.dist = 0
for i in range(len(nums)- 1):
    nums[i].after = nums[i+1]
    nums[i+1].before = nums[i]

nums[-1].after = nums[0]
nums[0].before = nums[-1]
nRound = 10
for _ in trange(nRound):
    for num in tqdm(nums, leave=False, position=1):
        num.move(num.dist)
    

#print('\n'.join([str(x) for x in nums]))
# 1, 2, -3, 4, 0, 3, -2

zero = None
for num in nums:
    if num.value == 0:
        zero = num
        break

tmp = zero
sum = 0
for __ in range(3):
    for _ in range(1000):
        tmp = tmp.after
    sum += tmp.value
    print(tmp.value)

print(sum)

