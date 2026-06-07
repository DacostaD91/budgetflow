from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = DATA_DIR / "budgetflow.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

APP_NAME = "BudgetFlow"
DEFAULT_CURRENCY = "DOP"
