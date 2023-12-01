values = {
    'A': 1,
    'B': 2,
    'C': 3,
}
to_win = {
    'A': 'B',
    'B': 'C',
    'C': 'A',
}
to_lose = {
    'A': 'C',
    'B': 'A',
    'C': 'B',
}

points = 0

with open('input', 'r') as f:
    for line in f:
        enemy, me = line.split(' ')
        me = me.strip()
        # x lose
        # y draw
        # z win
        if me == 'Z':
            points += 6
            points += values[to_win[enemy]]
        elif me == 'Y':
            points += 3
            points += values[enemy]
        elif me == 'X':
            points += values[to_lose[enemy]]


print(points)
#%%
