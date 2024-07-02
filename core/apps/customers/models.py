from uuid import uuid4

from django.db import models

from core.apps.common.models import TimeBaseModel
from core.apps.customers.entities import CustomerEntity


class Customer(TimeBaseModel):
    phone=models.CharField(
        verbose_name='Номер телефона',
        max_length=25,
        help_text='Напишите свой номер',
        unique=True,
    )
    token=models.CharField(
        verbose_name='Тикер для пользователя',
        max_length=255,
        default=uuid4(),
        unique=True,
    )
    
    def __str__(self) -> str:
        return self.phone

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            phone=self.phone,
            created_at=self.created_at,
        )
        
    class Meta:
        verbose_name='Customer'
        verbose_name_plural='Customers'
