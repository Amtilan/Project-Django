import pytest
from core.api.filters import PaginationIN
from tests.factories.products import ProductModelFactory

from core.api.v1.products.filters import ProductFilters
from core.apps.products.services.products import BaseProductService


@pytest.mark.django_db
def test_Products_count(product_service : BaseProductService):
    products_count=product_service.get_Product_Count(ProductFilters())
    
    assert products_count == 0, f'Product count: {products_count=}'


@pytest.mark.django_db
def test_Products_count_exist(product_service : BaseProductService):
    expected_products_count=5
    ProductModelFactory.create_batch(size=expected_products_count)
    
    products_count=product_service.get_Product_Count(ProductFilters())
    assert products_count == expected_products_count, f'Product count: {products_count=}'

    
@pytest.mark.django_db
def test_get_Products_all(product_service : BaseProductService):
    expected_products_count=5
    products=ProductModelFactory.create_batch(size=expected_products_count)
    products_titles={product.title for product in products}
    
    fetched_products=product_service.get_Product_List(ProductFilters(), pagination=PaginationIN())
    fetched_titles={product.title for product in fetched_products}
    assert len(fetched_titles) == expected_products_count, f'Product titles: {fetched_titles=}'
    assert products_titles == fetched_titles, f'Product titles: {products_titles=}'
    
