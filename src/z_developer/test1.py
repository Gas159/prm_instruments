fda = "fdas"
fds = "fds1 16.47 5, 16.56 5 17.03 8, 17.20  6 "

fruits = ["apple", "banana", "cherry", "date", "elderberry"]
index = fruits.index("cherry")
q = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(fruits)
w = "This website is for losers LOL!"
'''
[]                                -->  "no one likes this"
["Peter"]                         -->  "Peter likes this"
["Jacob", "Alex"]                 -->  "Jacob and Alex like this"
["Max", "John", "Mark"]           -->  "Max, John and Mark like this"
["Alex", "Jacob", "Mark", "Max"]  -->  "Alex, Jacob and 2 others like this"'''

def is_anagram(test, original):
    return sorted(test.lower()) == sorted(original.lower())

def likes(names):
    if len(names) == 0:
        'dFds'.lo
        return "no one likes this"
    elif len(names) == 1:
        return f"{names[0]} likes this"
    elif len(names) == 2:
        return f"{names[0]} and {names[1]} like this"
    elif len(names) == 3:
        return f'{names[0]}, {names[1]} and {names[2]} like this'
    elif len(names) > 3:
        return f"{names[0]}, {names[1]} and {len(names) - 2} others like this"



def digital_root(n):
    return n if n < 10 else digital_root(sum(map(int, str(n))))


print(digital_root(493193))


def create_phone_number(n):
    return f"({n[0:3]}) {n[3:6]}-{n[6:]}"


print(
    create_phone_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
)  # => returns "(123) 456-7890"


def descending_order(num):
    return int("".join(sorted(str(num), reverse=True)))


print(descending_order(123454))


def disemvowel(string_):
    vowels = "aeiouAEIOU"
    string_ = "".join(i for i in string_ if i not in vowels)
    return string_


print(disemvowel(w))


def square_digits(num):
    # Your code here1
    return int("".join(str(int(i) * 2) for i in str(num)))


print(square_digits(9119))


def remove_smallest(numbers):
    if numbers:
        res = numbers.copy()
        res.remove(min(res))
        return res
    return []


# q = [input('first num: '), input('second num: ')]
# print(q)
print(remove_smallest(q))


# def stranger_sum(
#     a: str = (input("first num: ")), b: str = input("second num: ")
# ) -> int:
#     max_lenght = max(len(a), len(b))
#     modified_a, modified_b = a.zfill(max_lenght), b.zfill(max_lenght)
#     res = []
#     for index in range(max_lenght):
#         res.append(str(int(modified_a[index]) + int(modified_b[index]))[-1])
#     return int("".join(res))


# print(stranger_sum())


# def func():
#     #     numb1 = input()
#     #     numb2 = input()
#     # numb1 = numb1.zfill(3)
#     # numb2 = numb2.zfill(3)
#     i = 0
#     total = ""
#     while i < 3:
#         i += 1
#         sum = int(numb1[-i]) + int(numb2[-i])
#         sum = str(sum)
#         total += sum[-1]
#     print(total[::-1])
