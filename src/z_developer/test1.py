fda = "fdas"
fds = "fds1"

# q = [input('first num: '), input('second num: ')]
# print(q)
q = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def stranger_sum(
    a: str = (input("first num: ")), b: str = input("second num: ")
) -> int:
    max_lenght = max(len(a), len(b))
    modified_a, modified_b = a.zfill(max_lenght), b.zfill(max_lenght)
    res = []
    for index in range(max_lenght):
        res.append(str(int(modified_a[index]) + int(modified_b[index]))[-1])
    return int("".join(res))

print(stranger_sum())

def func():
    numb1 = input()
    numb2 = input()
    numb1 = numb1.zfill(3)
    numb2 = numb2.zfill(3)
    i = 0
    total = ""
    while i < 3:
        i += 1
        sum = int(numb1[-i]) + int(numb2[-i])
        sum = str(sum)
        total += sum[-1]
    print(total[::-1])
