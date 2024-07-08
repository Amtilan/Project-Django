from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=True)
class ReviewInvalidRating(ServiceException):
    rating: int
    @property
    def message(self):
        return f"Raing {self.product_id=} not valid"