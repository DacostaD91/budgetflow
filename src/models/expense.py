from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, nullable=False, index=True)
    payment_method = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="expenses")
