"""
S = single responsibility
O = open/closed
L = Liskov substitution
I = interface segregation
D = dependency inversion

 одна область ответственности
"""


# bad example
class GenerateAndSend:
    def __init__(self, report):
        self.report = report

    def generate_and_send(self, pdf=True, excel=True, email=True, sms=True):
        print("generate report")
        print("send report")


# good example
class ReportGenerator:
    def __init__(self, report):
        self.report = report

    def generate(self):
        print("generate report")


class ReportSender:
    def __init__(self, report):
        self.report = report

    def send(self):
        print("send report")
