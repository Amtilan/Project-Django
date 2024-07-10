from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.exception.reviews import (
    ReviewInvalidRating,
    SingleReviewError,
)
from core.apps.products.models.reviews import ProductReview as ReviewModel


class BaseReviewService(ABC):
    @abstractmethod
    def check_review_Exist(
        self,
        product: ProductEntity,
        customer: CustomerEntity,
    ) -> bool:
        ...
        
    @abstractmethod
    def save_review(
        self, 
        product: ProductEntity,
        customer: CustomerEntity,
        review: ReviewEntity,
    ) -> ReviewEntity:
        ...
        
        
class ORMReviewService(BaseReviewService):
    def check_review_Exist(
        self,
        product: ProductEntity,
        customer: CustomerEntity,
    ) -> bool:
        return ReviewModel.objects.filter(
            product_id=product.id,
            customer_id=customer.id,
        ).exists()

    def save_review(
        self, 
        product: ProductEntity,
        customer: CustomerEntity,
        review: ReviewEntity,
    ) -> ReviewEntity:

        review_dto: ReviewModel=ReviewModel.from_entity(
            review=review,
            product=product,
            customer=customer,
        )
             
        review_dto.save()
        return review_dto.to_entity()
        
class BaseReviewValidatorService(ABC):
    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        product: ProductEntity | None = None,
    ):
        ...
        
        
class ReviewRatingValidatorService(BaseReviewValidatorService):
    def validate(
        self, 
        review: ReviewEntity, 
        *args,
        **kwargs,
    ):
        if not (0 <= review.rating <= 10): 
            raise ReviewInvalidRating(rating=review.rating)
    
@dataclass
class SingleReviewValidatorService(BaseReviewValidatorService):
    service: BaseReviewService
    
    def validate(
        self, 
        customer: CustomerEntity,
        product: ProductEntity,
        *args,
        **kwargs,
    ):
        if self.service.check_review_Exist(
            product=product,
            customer=customer,
        ):
            raise SingleReviewError(
                product_id=product.id, 
                customer_id=customer.id,
            )
        
        
@dataclass
class ComposedReviewValidatorService(BaseReviewValidatorService):
    validators: list[BaseReviewValidatorService]
    
    def validate(
        self, 
        review: ReviewEntity, 
        customer: CustomerEntity | None = None, 
        product: ProductEntity | None = None,
    ):
        for validator in self.validators:
            validator.validate(
                review=review,
                customer=customer,
                product=product,
            )
