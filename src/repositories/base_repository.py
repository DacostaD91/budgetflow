class BaseRepository:
    def __init__(self, db_session, model):
        self.db = db_session
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, entity_id: int):
        return self.db.query(self.model).filter(self.model.id == entity_id).first()

    def create(self, entity):
        self.db.add(entity)
        self.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity):
        self.db.delete(entity)
        self.commit()

    def commit(self):
        self.db.commit()
