from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIN
from core.apps.products.entities.products import Product
from core.apps.products.exception.products import ProductIDNotFoundException
from core.apps.products.filters.products import ProductFilters
from core.apps.products.models.products import Product as ProductDTO


class BaseProductService(ABC):
    @abstractmethod
    def get_Product_List(self, filters: ProductFilters, pagination: PaginationIN) -> Iterable[Product]:
        ... 
            
    @abstractmethod
    def get_Product_Count(self, filters: ProductFilters) -> int:
        ...
        
    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        ...

    @abstractmethod
    def get_all_products(self) -> Iterable[Product]:
        ...

class ORMProductService(BaseProductService):
    def __build_product_query(self, filters: ProductFilters) -> Q:
        query=Q(is_visible=True)
        
        if filters.search is not None:
            query &= (Q(title__icontains=filters.search) | Q(description__icontains=filters.search))
        
        return query
    
    def get_Product_List(self, filters: ProductFilters, pagination: PaginationIN) -> Iterable[Product]:
        query=self.__build_product_query(filters=filters)
        qs=ProductDTO.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]
    
        return [product.to_entity() for product in qs]
    
    def get_Product_Count(self, filters: ProductFilters) -> int:
        query=self.__build_product_query(filters=filters)
        
        return ProductDTO.objects.filter(query).count()
    
    def get_by_id(self, product_id: int) -> Product:
        try:
            proruct_dto=ProductDTO.objects.get(pk=product_id)
        except ProductDTO.DoesNotExist:
            raise ProductIDNotFoundException(product_id=product_id)
        return proruct_dto.to_entity()
    
    def get_all_products(self) -> Iterable[Product]:
        query=self.__build_product_query(filters=ProductFilters())
        queryset=ProductDTO.objects.filter(query)
        
        for product in queryset:
            yield product.to_entity()