from datetime import datetime
from typing import Optional
from ..schemas.user import UserOut

from pydantic import (
    BaseModel,
    conint,
)

from pydantic import EmailStr, ConfigDict


class BudgetBase(BaseModel):
    term: Optional[datetime]
    category: int
    amount: int


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class BudgetOut(BudgetBase):
    budget: Budget

    class Config:
        from_attributes = True
