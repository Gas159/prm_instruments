"""
L - liskov substitution
класс должен поддерживать изменения при изменении другого класса
"""

from abc import ABC, abstractmethod


# bad example
class BadBird(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def fly(self):
        pass

    @abstractmethod
    def swim(self):
        pass


class Eagle(BadBird):
    def fly(self):
        print("fly")

    def swim(self):
        raise NotImplemented("Eagle can't swim")

    @staticmethod
    def process_bird(self, bird: BadBird):
        bird.fly()
        bird.swim()


# good example
class Bird(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def fly(self):
        pass


class SwimmingBird(Bird):
    @abstractmethod
    def swim(self):
        pass


class Duck(SwimmingBird):
    def fly(self):
        print("fly")

    def swim(self):
        print("swim")

    def process_bird(self):
        print(self.name)
        self.fly()
        self.swim()


class Eagle(Bird):
    def fly(self):
        print("fly")

    def process_bird(self):
        self.fly()


def process_bird1(bird: Bird):
    bird.fly()


eagle = Eagle(name="Eagle")
eagle.process_bird()

duck = Duck(name="Duck")
duck.process_bird()
