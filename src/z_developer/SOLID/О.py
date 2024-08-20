"""
O - open/close
класс должен быть открыть для расширения, но закрыть для изменения
"""

import math
from abc import ABC, abstractmethod


# bad
class BadShape(ABC):
    def __init__(self, name, radius=None, side=None):
        self.name = name
        self.radius = radius
        self.side = side

    def area(self):
        if self.name == "circle":
            return math.pi * self.radius**2
        elif self.name == "square":
            return self.side**2
        elif self.name == "triangle":
            return self.side / 2 * math.sqrt(3)
        else:
            return


# good example
class Shape(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, name, radius):
        self.radius = radius
        self.name = super().__init__(name)

    def area(self):
        return self.radius, self.name, math.pi * self.radius**2


class Square(Shape):
    def __init__(self, side, name):
        self.side = side
        super().__init__(name)

    def area(self):
        return self.name, self.side, self.side**2


q = Circle(name="circle", radius=5)
print(q.area())

w = Square(name="square", side=5)
print(w.area())
