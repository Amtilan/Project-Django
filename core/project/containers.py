from functools import lru_cache
from logging import (
    getLogger,
    Logger,
)

from django.conf import settings

import punq
from httpx import Client

from core.apps.common.clients.elasticsearch import ElasticClient
from core.apps.customers.services.auth import (
    AuthService,
    BaseAuthService,
)
from core.apps.customers.services.codes import (
    BaseCodeService,
    DjangoCacheCodeService,
)
from core.apps.customers.services.customers import (
    BaseCustomerService,
    ORMCustomerService,
)
from core.apps.customers.services.senders import (
    BaseSendersService,
    ComposeSendersService,
    EmailSendersService,
    PushSendersService,
)
from core.apps.products.services.products import (
    BaseProductService,
    ORMProductService,
)
from core.apps.products.services.reviews import (
    BaseReviewService,
    BaseReviewValidatorService,
    ComposedReviewValidatorService,
    ORMReviewService,
    ReviewRatingValidatorService,
    SingleReviewValidatorService,
)
from core.apps.products.services.search import (
    BaseSearchProductService,
    ElasticSearchService,
)
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.apps.products.use_cases.search.upsert_search_data import UpsertSearchDataUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()
    
def _initialize_container() -> punq.Container:
    
    def build_validators() -> BaseReviewValidatorService:
        return ComposedReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService),
            ],
        )
    
    def build_elastic_search_service() -> BaseSearchProductService:
        return ElasticSearchService(
            client=ElasticClient(
                http_client=Client(base_url=settings.ELASTIC_URL),
            ),
            index_name=settings.ELASTIC_PRODUCT_INDEX,
        )

        
    container=punq.Container()
    
    container.register(BaseProductService, ORMProductService)
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(
        BaseSendersService, ComposeSendersService, sender_services=(
        PushSendersService(), 
        EmailSendersService(),
        ),
    )
    container.register(BaseAuthService, AuthService)
    
    
    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)
    container.register(BaseReviewService, ORMReviewService)
    container.register(BaseReviewValidatorService, factory=build_validators)
    container.register(CreateReviewUseCase)
    container.register(Logger, factory=getLogger, name='django.request')
    container.register(BaseSearchProductService, factory=build_elastic_search_service)
    
    
    container.register(UpsertSearchDataUseCase)
    return container