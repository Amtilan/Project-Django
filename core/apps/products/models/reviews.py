from django.db import models

from core.apps.common.models import TimeBaseModel
from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import Review as ReviewEntity


class ProductReview(TimeBaseModel):
    customer=models.ForeignKey(
        to='customers.Customer',
        verbose_name='Reviewer',
        related_name='Product_Reviews',
        on_delete=models.CASCADE,
    )
    product=models.ForeignKey(
        to='products.Product',
        verbose_name='Product',
        related_name='Product_Reviews',
        on_delete=models.CASCADE,
    )
    text=models.TextField(
        verbose_name='Review text',
        blank=True,
        default='',
    )
    rating=models.PositiveSmallIntegerField(
        verbose_name='Cutomer Rating',
        default=1,
    )
    
    @classmethod
    def from_entity(
        cls,
        review: ReviewEntity,
        product: ProductEntity,
        customer: CustomerEntity,
    ) -> 'ProductReview':
        
        return cls(
            pk=review.id,
            product_id=product.id,
            customer_id=customer.id,
            text=review.text,
            rating=review.rating,
        )
    
    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            id=self.pk,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
    
    class Meta:
        verbose_name='Product review'
        verbose_name_plural='Product reviews'
        unique_together=(
            ('customer','product'),
        )