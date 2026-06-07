from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    income_date = Column(Date, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="incomes")
