from src.core.exceptions import ValidationException
from src.models.category import Category
from src.repositories.category_repository import CategoryRepository
from src.schemas.category_schema import CategoryCreateSchema
from src.utils.validators import validate_required_text

VALID_CATEGORY_TYPES = {"income", "expense"}


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(self, category_data: CategoryCreateSchema) -> Category:
        validate_required_text(category_data.name, "Category name")

        if category_data.type not in VALID_CATEGORY_TYPES:
            raise ValidationException("Category type must be either income or expense.")

        if self.category_repository.get_by_name(category_data.name):
            raise ValidationException("Category already exists.")

        category = Category(
            name=category_data.name.strip(),
            type=category_data.type,
            description=category_data.description,
        )
        return self.category_repository.create(category)

    def get_all_categories(self):
        return self.category_repository.get_all()

    def get_expense_categories(self):
        return self.category_repository.get_by_type("expense")

    def get_income_categories(self):
        return self.category_repository.get_by_type("income")
