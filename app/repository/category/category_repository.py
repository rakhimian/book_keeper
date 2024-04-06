"""
Модуль описывает репозиторий, работающий c PostgreSql
"""

from itertools import count
from typing import Any

from app.repository.category.abstract_category_repository import AbstractCategoryRepository, T


class CategoryRepository(AbstractCategoryRepository):
    """
        Репозиторий, работающий с базой данных PostgreSQL. Хранит данные в таблицах базы данных PostgreSQL.
    """

    def add(self, obj: T) -> int:
        pass

    def get(self, pk: int) -> T | None:
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)
