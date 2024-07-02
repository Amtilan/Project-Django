import random
import string
from abc import (
    ABC,
    abstractmethod,
)

from django.core.cache import cache

from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exception.codes import (
    CodeNotEqual,
    CodeNotFoundException,
)


class BaseCodeService(ABC):
    @abstractmethod
    def generate_auth_code(self, customer: CustomerEntity) -> str:
        ...
    
    @abstractmethod
    def validate_auth_code(self, code: str, customer: CustomerEntity) -> None:        
        ...
        
    

class DjangoCacheCodeService(BaseCodeService):
    def generate_auth_code(self, customer: CustomerEntity) -> str:
        auth_code=''.join(random.choices(string.digits, k=6))
        cache.set(customer.phone, auth_code)
        return auth_code
        
    def validate_auth_code(self, code: str, customer: CustomerEntity) -> None:
        cache_code=cache.get(customer.phone, code)
        
        if cache_code is None: 
            raise CodeNotFoundException(code=code)
        
        if cache_code != code:
            raise CodeNotEqual(code=code,cached_code=cache_code, customer_phone=customer.phone)
        
        cache.delete(customer.phone)
