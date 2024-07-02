from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSendersService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    codes_service: BaseCodeService
    sender_service: BaseSendersService
    
    @abstractmethod
    def authorize(self, phone: str) -> None:
        ...
    
    @abstractmethod
    def confirm(self, code: str, phone: str):
        ...
        
class AuthService(BaseAuthService):
    def authorize(self, phone: str) -> None:
        customer=self.customer_service.get_or_create_customer(phone=phone)
        code=self.codes_service.generate_auth_code(customer=customer)
        self.sender_service.send_auth_code(auth_code=code, customer=customer)
        
    def confirm(self, code: str, phone: str):
        customer=self.customer_service.get_customer(phone=phone)
        self.codes_service.validate_auth_code(code=code, customer=customer)
        return self.customer_service.generate_token(customer=customer)