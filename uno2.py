from tqdm import tqdm

with open('input', 'r') as f:
    first = 0
    second = 0
    third = 0
    elf = 0
    for line in tqdm(f):
        if line == '\n':
            if elf > first:
                third = second
                second = first
                first = elf
            elif elf > second:
                third = second
                second = elf
            elif elf > third:
                third = elf

            elf = 0
        else:
            elf += int(line)
    if elf > first:
        third = second
        second = first
        first = elf
    elif elf > second:
        third = second
        second = elf
    elif elf > third:
        third = elf

    print(str(first+second+third))

#%%
