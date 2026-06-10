from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.settings import DATA_DIR, DATABASE_URL

DATA_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session() -> Generator:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def init_database() -> None:
    from src.models.category import Category  # noqa: F401
    from src.models.debt import Debt  # noqa: F401
    from src.models.debt_payment import DebtPayment  # noqa: F401
    from src.models.expense import Expense  # noqa: F401
    from src.models.income import Income  # noqa: F401
    from src.models.monthly_budget import MonthlyBudget  # noqa: F401

    Base.metadata.create_all(bind=engine)
