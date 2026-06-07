# BudgetFlow

BudgetFlow is a personal finance management application built with Python, Streamlit, SQLite and SQLAlchemy.

## Features in this first version

- Project structure
- SQLite database setup
- SQLAlchemy models
- Repository layer
- Service layer
- Streamlit UI skeleton
- Income registration
- Expense registration
- Monthly dashboard summary

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

## How to run

1. Create virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
streamlit run app.py
```

## How to run tests

```bash
pytest
```
