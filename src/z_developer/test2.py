#
# var = {
# 	1: 1,
# 	True: 2,
# 	1.0: 3,
# 	"1": 4
# }

# print(var)

# {1:3, '1': 4}


class A:
    def __hash__(self):
        return 1

    # def __eq__(self, other):
    #     return isinstance(other, A)  # Сравнение по типу

    # def __str__(self):
    #     return "A"


class B:
    def __hash__(self):
        return 1

    #
    # def __eq__(self, other):
    #     return isinstance(other, B)  # Сравнение по типу

    def __str__(self):
        return "B"


print(A())
print(B())
print(A() == B())
print()
var = {A(): 1, B(): 2}
print(var)
# print(var[A()])  # Вывод: 1
# print(var[B()], var[A()])  # Вывод: 2


#
# ---
# slot = type(A, __slot__, ('a','b'))

#
class A:
    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a = a
        self.b = b
        # self.c = c


class B(A):
    __slots__ = ("c",)

    def __init__(self, a, b, c):
        self.c = c
        super().__init__(a, b)

    def __str__(self):
        return f"B: [{self.a}] [{self.b}] [{self.c}]"


# a = A(1, 2, 3)
# print(type(a), a.a, a.b, dir(a))
b = B(1,2,3)
print(B(1, 2, 3))
print(B.__slots__)
print(A.__slots__)
# #
# # raise C
