from src.core.database import SessionLocal
from src.repositories.budget_repository import BudgetRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.debt_payment_repository import DebtPaymentRepository
from src.repositories.debt_repository import DebtRepository
from src.repositories.expense_repository import ExpenseRepository
from src.repositories.income_repository import IncomeRepository
from src.services.budget_service import BudgetService
from src.services.category_service import CategoryService
from src.services.debt_service import DebtService
from src.services.expense_service import ExpenseService
from src.services.income_service import IncomeService
from src.services.report_service import ReportService


def get_category_service() -> CategoryService:
    db_session = SessionLocal()
    category_repository = CategoryRepository(db_session)
    return CategoryService(category_repository)


def get_income_service() -> IncomeService:
    db_session = SessionLocal()
    income_repository = IncomeRepository(db_session)
    category_repository = CategoryRepository(db_session)
    return IncomeService(income_repository, category_repository)


def get_expense_service() -> ExpenseService:
    db_session = SessionLocal()
    expense_repository = ExpenseRepository(db_session)
    category_repository = CategoryRepository(db_session)
    return ExpenseService(expense_repository, category_repository)


def get_report_service() -> ReportService:
    db_session = SessionLocal()
    income_repository = IncomeRepository(db_session)
    expense_repository = ExpenseRepository(db_session)
    return ReportService(income_repository, expense_repository)


def get_budget_service() -> BudgetService:
    db_session = SessionLocal()
    budget_repository = BudgetRepository(db_session)
    category_repository = CategoryRepository(db_session)
    expense_repository = ExpenseRepository(db_session)
    return BudgetService(budget_repository, category_repository, expense_repository)


def get_debt_service() -> DebtService:
    db_session = SessionLocal()
    debt_repository = DebtRepository(db_session)
    debt_payment_repository = DebtPaymentRepository(db_session)
    return DebtService(debt_repository, debt_payment_repository)
