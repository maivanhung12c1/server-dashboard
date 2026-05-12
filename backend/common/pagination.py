import math
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: list[T], total: int, page: int, size: int) -> "PageData[T]":
        total_pages = math.ceil(total / size) if size > 0 else 0
        return cls(items=items, total=total, page=page, size=size, total_pages=total_pages)