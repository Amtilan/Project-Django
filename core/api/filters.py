from enum import Enum
from typing import Any

from ninja import Schema


class PaginationOUT(Schema):
    offset: int
    limit: int
    total: int
    

class PaginationIN(Schema):
    offset: int=0
    limit: int=20
    
class defaultFilter(Enum):
    NOT_SET: Any