from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=True)
class ProductIDNotFoundException(ServiceException):
    product_id: int
    @property
    def message(self):
        return f"Product {self.product_id=} not found"