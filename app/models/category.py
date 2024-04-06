"""
    Модель категории расходов
"""

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..repository.database import Base


@dataclass
class Category(Base):
    """
        Категория расходов, хранит название в атрибуте name и ссылку (id) на
        родителя (категория, подкатегорией которой является данная) в атрибуте parent.
        У категорий верхнего уровня parent = None
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    parent = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

