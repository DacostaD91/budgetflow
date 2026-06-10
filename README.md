# BudgetFlow

BudgetFlow is a personal finance management application built with Python, Streamlit, SQLite and SQLAlchemy.

## Current Features

- Streamlit user interface
- SQLite database setup
- SQLAlchemy models
- Repository layer
- Service layer
- Monthly dashboard summary
- Income registration and editing
- Expense registration and editing
- Monthly filters for incomes and expenses
- Manual generation of recurring income and expense entries
- Monthly budgets by expense category
- Budget vs actual expense comparison
- Budget summary metrics and charts
- Debt management
- Debt payment registration
- Debt balance and progress tracking
- Basic analytics and automated tests

## Tech Stack

- Python
- Streamlit
- SQLite
- SQLAlchemy
- Pandas
- Plotly
- pytest

## Architecture

Presentation Layer -> Service Layer -> Repository Layer -> SQLAlchemy ORM -> SQLite

BudgetFlow follows a layered architecture:

- Presentation Layer: Streamlit pages and UI components
- Service Layer: validation, business rules and calculations
- Repository Layer: database access
- Data Layer: SQLAlchemy models and SQLite
- Analytics: reusable financial calculations

## Modules

### Dashboard

Shows a monthly summary with total income, total expenses and net balance.

### Incomes

Allows registering, editing and viewing incomes by selected month. Recurring incomes can be manually generated for the selected month from previous recurring records.

### Expenses

Allows registering, editing and viewing expenses by selected month. Recurring expenses can be manually generated for the selected month from previous recurring records.

### Budgets

Allows creating monthly budgets by expense category, comparing planned amounts against actual expenses, reviewing usage percentages and identifying overbudget categories.

### Debts

Allows creating debts, registering payments, tracking remaining balances, viewing active and paid debts, and reviewing payment history.

## How to run

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
streamlit run app.py
```

The app will create the local SQLite database at:

```text
data/budgetflow.db
```

## How to run tests

```bash
pytest
```

## Database

BudgetFlow currently uses SQLite. The database file is intentionally ignored by Git:

```text
data/budgetflow.db
```

The `data/.gitkeep` file is tracked so the data directory exists in fresh clones.

## Project Structure

```text
app.py
src/
  analytics/
  core/
  models/
  repositories/
  schemas/
  seed/
  services/
  ui/
  utils/
tests/
data/
```

## Known Limitations

- No authentication or multi-user support yet.
- No cloud deployment setup yet.
- Debt payments do not automatically create expense records.
- Recurring entries are generated manually, not automatically.
- No CSV or Excel import/export yet.
- No advanced amortization or interest calculations yet.
