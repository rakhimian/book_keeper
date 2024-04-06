from datetime import datetime
from typing import Optional
from ..schemas.user import UserOut

from pydantic import (
    BaseModel,
    conint,
)
from pydantic import EmailStr, ConfigDict


class CategoryBase(BaseModel):
    name: str
    parent: int


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class CategoryOut(CategoryBase):
    category: Category

    class Config:
        from_attributes = True
