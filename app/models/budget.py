# time limit
# expense category
# sum
#
# срок
# категория расходов
# сумма

"""
Описан класс, представляющий модель бюджета
"""


from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..repository.database import Base


@dataclass()
class Budget(Base):
    """
    Бюджет.

    id - id записи в базе данных
    term - срок
    category - id категории расходов
    amount - сумма
    created_at - дата добавления в бд
    owner_id - id владельца записи
    owner - референс на владельца записи
    """

    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, nullable=False)
    term = Column(TIMESTAMP(timezone=True), nullable=True)
    category = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
