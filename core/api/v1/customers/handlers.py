from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    AuthInSchema,
    AuthOutSchema,
    TokenCodeSchema,
    TokenInSchema,
)
from core.apps.common.exception import ServiceException
from core.apps.customers.services.auth import BaseAuthService
from core.project.containers import get_container


router=Router(tags=['Customers'])

@router.post('auth', response=ApiResponse[AuthOutSchema], operation_id='authorize')
def auth_handler(
    request: HttpRequest, 
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    container=get_container()
    service: BaseAuthService=container.resolve(BaseAuthService)
    service.authorize(phone=schema.phone)
    return ApiResponse(data=AuthOutSchema(message=f'Code sended to: {schema.phone}'))

@router.post('get_token', response=ApiResponse[TokenCodeSchema], operation_id='get_token')
def get_token_handler(
    request: HttpRequest, 
    schema: TokenInSchema,
) -> ApiResponse[TokenCodeSchema]:
    container=get_container()
    service: BaseAuthService=container.resolve(BaseAuthService)
    try:
        token=service.confirm(code=schema.code, phone=schema.phone)
    except ServiceException as exception:
        raise HttpError(
            status_code=400, 
            message=exception.message,
        ) from exception
    
    
    return ApiResponse(data=TokenCodeSchema(token=token))