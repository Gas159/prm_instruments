from abc import ABC, abstractmethod


class AbstactSMSProvider(ABC):
    @abstractmethod
    def send_sms(self, message: str, to: str) -> tuple[bool, str]:
        pass

    def send_sms1(self, message: str, to: str) -> tuple[bool, str]:
        raise NotImplementedError


class AeroSMSProvider(AbstactSMSProvider):
    def send_sms(self, message: str, to: str) -> tuple[bool, str]:
        return True, "success"


def send_sms(provider: AbstactSMSProvider):
    provider.send_sms(message="hello", to="123")


sms = AeroSMSProvider()
