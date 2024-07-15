
from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.common.clients.elasticsearch import ElasticClient
from core.apps.products.entities.products import Product


@dataclass
class BaseSearchProductService(ABC):
    @abstractmethod
    def upsert_product(self, product: Product) -> None:
        ...
        
@dataclass
class ElasticSearchService(BaseSearchProductService):
    client: ElasticClient
    index_name: str
    
    @staticmethod
    def _build_as_document(product: Product) -> dict:
        return {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'tags': product.tags,
        }
    
    def upsert_product(self, product: Product) -> None:
        self.client.upsert_index(
            index=self.index_name,
            document_id=product.id,
            document=self._build_as_document(product=product),
        )