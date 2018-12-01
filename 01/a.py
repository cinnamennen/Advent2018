total = 0

with open('a.txt') as f:
    for line in f.readlines():
        total +=(int(line.strip()))

print(total)