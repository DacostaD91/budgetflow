from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    type = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)

    incomes = relationship("Income", back_populates="category")
    expenses = relationship("Expense", back_populates="category")
