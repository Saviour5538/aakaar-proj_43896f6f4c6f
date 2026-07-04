from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDService(Generic[ModelType]):
    """Generic CRUD service for SQLAlchemy models."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> ModelType:
        """Create a new record."""
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error creating {self.model.__name__}: {str(e)}")

    def read(self, db: Session, id: str) -> Optional[ModelType]:
        """Read a record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, id: str, obj_in: dict) -> Optional[ModelType]:
        """Update a record by ID."""
        db_obj = self.read(db, id)
        if not db_obj:
            return None
        try:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error updating {self.model.__name__}: {str(e)}")

    def delete(self, db: Session, id: str) -> bool:
        """Delete a record by ID."""
        db_obj = self.read(db, id)
        if not db_obj:
            return False
        try:
            db.delete(db_obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error deleting {self.model.__name__}: {str(e)}")

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """List records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()