from django.http import HttpRequest
from ninja import Query, Router

from core.api.filters import PaginationIN
from core.api.schemas import ApiResponse, ListPaginatedResponse, PaginationOUT
from core.api.v1.products.filters import ProductFilters
from core.api.v1.products.schemas import ProductSchema
from core.apps.products.services.products import BaseProductService, ORMProductService

router = Router(tags = ['Produts'])

@router.get('', response = ApiResponse[ListPaginatedResponse[ProductSchema]])
def get_product_list_handler(
    request : HttpRequest, 
    filters : Query[ProductFilters], 
    pagination_in : Query[PaginationIN]
) -> ApiResponse[ListPaginatedResponse[ProductSchema]]:
    service: BaseProductService = ORMProductService()
    product_list = service.get_Product_List(filters=filters, pagination=pagination_in)
    product_count = service.get_Product_Count(filters=filters)
    items = [ProductSchema.from_entity(abc) for abc in product_list]
    
    pagination_out = PaginationOUT(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=product_count,
    )
    return ApiResponse(
        data = ListPaginatedResponse(
            items=items, 
            pagination=pagination_out
        )
    )