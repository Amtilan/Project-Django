from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI

from scalar_django_ninja import ScalarViewer

from core.api.schemas import PingResponseSchema
from core.api.v1.urls import router as v1_router


api=NinjaAPI(
    docs=ScalarViewer(),
)


@api.get("/ping", response=PingResponseSchema)
def ping(request: HttpRequest) -> PingResponseSchema:
    return PingResponseSchema(result=True)


api.add_router('v1/', v1_router)


urlpatterns=[
    path("", api.urls),    
]