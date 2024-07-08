from django.db import models

from core.apps.common.models import TimeBaseModel

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
    class Meta:
        verbose_name='Product review'
        verbose_name_plural='Product reviews'
        unique_together=(
            ('customer','product',),
        )