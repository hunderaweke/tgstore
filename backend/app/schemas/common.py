from enum import Enum as PyEnum
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class SortOrder(str, PyEnum):
    asc = "asc"
    desc = "desc"


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
    ):
        self.page = page
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class Page(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool

    @classmethod
    def create(cls, items: list[T], total: int, pagination: PaginationParams) -> "Page[T]":
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            has_next=pagination.offset + len(items) < total,
        )
