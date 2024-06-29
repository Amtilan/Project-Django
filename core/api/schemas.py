from typing import (
    Any,
    Generic,
    TypeVar,
)

from ninja import Schema

from pydantic import Field

from core.api.filters import PaginationOUT


TData=TypeVar("TData")
TListItem=TypeVar("TListItem")

class PingResponseSchema(Schema):
    result: bool
    


class ListPaginatedResponse(Schema, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOUT


class ApiResponse(Schema, Generic[TData]):
    data: TData | dict=Field(default_factory=dict)
    meta: dict[str, Any]=Field(default_factory=dict)
    errors: list[Any]=Field(default_factory=list)