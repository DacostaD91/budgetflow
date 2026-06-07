class BudgetFlowException(Exception):
    """Base exception for BudgetFlow."""


class NotFoundException(BudgetFlowException):
    """Raised when an entity is not found."""


class ValidationException(BudgetFlowException):
    """Raised when validation fails."""


class DatabaseException(BudgetFlowException):
    """Raised when a database operation fails."""
