from src.models.category import Category
from src.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Category)

    def get_by_name(self, name: str):
        return self.db.query(Category).filter(Category.name == name).first()

    def get_by_type(self, category_type: str):
        return self.db.query(Category).filter(Category.type == category_type).all()
