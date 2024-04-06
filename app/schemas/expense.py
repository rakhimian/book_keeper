from datetime import datetime
from typing import Optional
from ..schemas.user import UserOut

from pydantic import (
    BaseModel,
    conint,
)

from pydantic import EmailStr, ConfigDict


class ExpenseBase(BaseModel):
    category: int
    amount: int
    comment: str
    expense_date: Optional[str] = datetime.now()


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    created_at: datetime
    expense_date: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class ExpenseOut(ExpenseBase):
    expense: Expense

    class Config:
        from_attributes = True
