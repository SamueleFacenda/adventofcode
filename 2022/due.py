values = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}
wins = {
    'X': 'C',
    'Y': 'A',
    'Z': 'B',
}
loses = {
    'X': 'B',
    'Y': 'C',
    'Z': 'A',
}

points = 0

with open('input', 'r') as f:
    for line in f:
        enemy, me = line.split(' ')
        me = me.strip()
        points += values[me]
        if wins[me] == enemy:
            points += 6
        elif loses[me] != enemy:
            points += 3


print(points)
#%%
