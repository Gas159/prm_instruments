"""
I - Interface Segregation Principle

Клиенты не должны зависеть от методов, которые они не используют.
"""

from abc import abstractmethod, ABC


# bad example
class MultifuncDevice:
    def print(self, document):
        print("Printing...")

    def scan(self, document):
        print("Scanning...")

    def fax(self, document):
        print("Faxing...")


class Printer(MultifuncDevice):
    def print(self, document):
        print("Printing...")

    def scan(self, document):
        raise NotImplemented("Printer can't scan")


# good example
class Printer(ABC):
    def __init__(self, document):
        self.document = document

    @abstractmethod
    def print(self, document): ...


class Scanner:
    def scan(self, document): ...


class Fax:
    def fax(self, document): ...


class SimplePrinter(Printer):
    def __init__(self, document):
        super().__init__(document)

    def print(self, document):
        print("Printing...")


class MultiPrinter(Printer, Scanner, Fax):
    def __init__(self, document):
        super().__init__(document)

    def print(self, document):
        print("Printing multiprinter...")

    def scan(self, document):
        print("Scanning...")

    def fax(self, document):
        print("Faxing...")
