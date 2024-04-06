from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    conint,
)
from pydantic import EmailStr, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: Optional[str] = None

