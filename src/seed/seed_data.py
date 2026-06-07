from src.core.database import SessionLocal
from src.models.category import Category

DEFAULT_INCOME_CATEGORIES = [
    "Salary",
    "Bonus",
    "Freelance",
    "Investment",
    "Other Income",
]

DEFAULT_EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Housing",
    "Debt Payment",
    "Education",
    "Health",
    "Gym",
    "Entertainment",
    "Savings",
    "Other Expense",
]


def seed_default_categories() -> None:
    db_session = SessionLocal()
    try:
        _seed_categories(db_session, DEFAULT_INCOME_CATEGORIES, "income")
        _seed_categories(db_session, DEFAULT_EXPENSE_CATEGORIES, "expense")
        db_session.commit()
    finally:
        db_session.close()


def _seed_categories(db_session, names: list[str], category_type: str) -> None:
    for name in names:
        exists = db_session.query(Category).filter(Category.name == name).first()
        if not exists:
            db_session.add(Category(name=name, type=category_type))
