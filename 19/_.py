data = [_.strip() for _ in open('a.txt').readlines()]
for i,d in enumerate(data[1:]):
    print(f"""
def f{i}(registers, ip):
    # {d}
    return ip
    """)
