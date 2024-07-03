from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from core.apps.customers.entities import CustomerEntity


class BaseSendersService(ABC):
    @abstractmethod
    def send_auth_code(self, auth_code: str) -> None:
        ...
        
class DummySendersService(BaseSendersService):
    def send_auth_code(self, auth_code: str, customer: CustomerEntity) -> None:
        print(f"Sending {customer=} auth code {auth_code=}")

class EmailSendersService(BaseSendersService):
    def send_auth_code(self, customer: CustomerEntity, auth_code: str) -> None:
        print(f"Sending {customer=} auth code {auth_code=}")
        
class PushSendersService(BaseSendersService):
    def send_auth_code(self, customer: CustomerEntity, auth_code: str) -> None:
        print(f"Sending push notification auth code {auth_code=}")
                
@dataclass
class ComposeSendersService(BaseSendersService):
    sender_services: Iterable[BaseSendersService]
    def send_auth_code(self, customer: CustomerEntity, auth_code: str) -> None:
        for service in self.sender_services:
            service.send_auth_code(customer, auth_code)