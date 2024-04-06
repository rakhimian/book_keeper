"""
Описан класс, представляющий расходную операцию
"""


from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..repository.database import Base


@dataclass()
class Expense(Base):
    """
    Расходная операция.

    id - id записи в базе данных
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    comment - комментарий
    created_at - дата добавления в бд
    owner_id - id владельца записи
    owner - референс нв ладельца записи
    """

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Integer, nullable=False)
    category = Column(Integer, ForeignKey("categories.id"), nullable=False)
    expense_date = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    comment = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
