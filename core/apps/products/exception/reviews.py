from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=True)
class ReviewInvalidRating(ServiceException):
    rating: int
    @property
    def message(self):
        return f"Rating {self.rating} not valid on product"
    

@dataclass(eq=True)
class SingleReviewError(ServiceException):
    product_id: int
    customer_id: int
    @property
    def message(self):
        return f"Product {self.product_id} has too many reviews from customer {self.customer_id}"