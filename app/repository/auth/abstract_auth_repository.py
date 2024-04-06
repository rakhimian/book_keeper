"""
Модуль содержит описание абстрактного репозитория
"""

from abc import ABC, abstractmethod
from fastapi import HTTPException
from app.schemas import auth as auth_schema


class AbstractAuthRepository(ABC):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
        - get_current_user
    """

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str, credentials_exception: HTTPException) -> auth_schema.TokenData:
        pass
