from datetime import datetime

from django.http import HttpRequest
from ninja import (
    Header,
    Query,
    Router,
)
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.reviews.schemas import (
    CreateReviewInSchema,
    ReviewInSchema,
    ReviewOutSchema,
)
from core.apps.common.exception import ServiceException
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.project.containers import get_container


router=Router(tags=['Reviews'])

@router.post('products/{product_id}/reviews', response=ApiResponse[ReviewOutSchema], operation_id='create_review')
def create_review(
    request: HttpRequest, 
    product_id: int,
    schema: ReviewInSchema,
    token: str=Header(alias='Auth-Token'),
) -> ApiResponse[ReviewOutSchema]:
    container=get_container()
    use_case: CreateReviewUseCase=container.resolve(CreateReviewUseCase)
    try:
        result=use_case.execute(
            product_id=product_id,
            customer_token=token,
            review=schema.to_entity(),
        )
    except ServiceException as error:
        raise HttpError(
            status_code=400,
            message=error.message,
        )
    
    return ApiResponse(data=ReviewOutSchema.from_entity(review=result))
    