"""
D - Dependency Inversion Principle

Модули верхнего уровня не должны зависеть от модулей нижнего уровня,
модули нижнего уровня должны зависеть от модулей верхнего уровня, оба должны зависеть от абстракции.
Абстракции не должны зависеть от деталей, детали должны зависеть от абстракции.
"""

from abc import abstractmethod, ABC

#
# class LightLamp:
#     def turn_on(self):
#         print("Lamp is on")
#
#     def turn_off(self):
#         print("Lamp is off")
#
#
# class LightSwitch:
#     def __init__(self, device: LightLamp):
#         self.device = device
#
#     def operate(self):
#         self.device.turn_on()
#         # some logic for off_lamp
#         self.device.turn_off()
#
#
# light_lamp = LightLamp()
# lamp = LightSwitch(light_lamp)
# lamp.operate()


# Good example
class Switchable(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class LightLamp(Switchable):
    def turn_on(self):
        print("Lamp is on")

    def turn_off(self):
        print("Lamp is off")


class Conditioner(Switchable):
    def turn_on(self):
        print("conditioner is on")

    def turn_off(self):
        print("conditioner is off")


class Switch:
    def __init__(self, device: Switchable):
        self.device = device

    def run_proccess(self):
        self.device.turn_on()
        # some logic for turn_off
        self.device.turn_off()


light_lamp = LightLamp()
light_lamp_switch = Switch(light_lamp)
light_lamp_switch.run_proccess()

conditioner = Conditioner()
conditioner_switch = Switch(conditioner)
conditioner_switch.run_proccess()
