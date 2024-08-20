from abc import ABC, abstractmethod


class AbstactSMSProvider(ABC):
    @abstractmethod
    def send_sms(self, message: str, to: str) -> tuple[bool, str]:
        pass


class AeroSMSProvider(AbstactSMSProvider):
    def send_sms(self, message: str, to: str) -> tuple[bool, str]:
        pass



sms = AeroSMSProvider()
