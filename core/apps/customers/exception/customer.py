from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=True)
class CustomerTokenNotFoundException(ServiceException):
    token: str
    @property
    def message(self):
        return f"Customer {self.token=} not found"