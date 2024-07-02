from abc import (
    ABC,
    abstractmethod,
)

from core.apps.customers.entities import CustomerEntity


class BaseSendersService(ABC):
    @abstractmethod
    def send_auth_code(self, auth_code: str) -> None:
        ...
        
class DummySendersService(BaseSendersService):
    def send_auth_code(self, auth_code: str, customer: CustomerEntity) -> None:
        print(f"Sending {customer=} auth code {auth_code=}")
