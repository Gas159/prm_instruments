class A:
    __slots__ = ("a", "b")

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"A: [{self.a}] [{self.b}] [{self.c}]"


print(A(1, 2, 3))
