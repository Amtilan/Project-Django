from django.db import models

from core.apps.common.models import TimeBaseModel
from core.apps.products.entities.products import Product as ProductEntity


class Product(TimeBaseModel):
    title=models.CharField(
        max_length=255,
        verbose_name='Название товара',
    )
    description=models.TextField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Описание товара',
    )
    is_visible=models.BooleanField(
        default=True,
        verbose_name='Виден ли товар в каталоге',
    )
    
    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            id=self.pk,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name='Товар'
        verbose_name_plural='Товары'