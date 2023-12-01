from tqdm import tqdm

with open('input', 'r') as f:
    higher = 0
    elf = 0
    for line in tqdm(f):
        if line == '\n':
            if elf > higher:
                higher = elf
            elf = 0
        else:
            elf += int(line)

    if elf > higher:
        higher = elf

print(higher)
