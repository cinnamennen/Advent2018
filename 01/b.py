current = 0
changes = []
observed = [0]

with open('a.txt') as f:
    for line in f.readlines():
        changes.append(int(line.strip()))


while True:
    for freq in changes:
        # print(f'current: {current} freq: {freq}')
        current += freq
        # print(f'res: {current}')
        if current in observed:
            print(current)
            exit()
        else:
            observed.append(current)

