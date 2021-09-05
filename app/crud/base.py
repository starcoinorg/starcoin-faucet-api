from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.db.base_class import Page
from app.utils import paginate

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, filter_by: Dict = None, page_num: int = 1, page_size: int = 100
    ) -> Page:
        q = db.query(self.model)
        if filter_by:
            filter_by = {k: v for k, v in filter_by.items() if v is not None}
            q = q.filter_by(**filter_by)
        return paginate(page_num=page_num, page_size=page_size, query=q)

    def get_multi_by_ids(self, db: Session, *, ids: List[int], page_num: int = 1, page_size: int = 100) -> Page:
        q = db.query(self.model).filter(self.model.id.in_(ids))
        return paginate(page_num=page_num, page_size=page_size, query=q)

    def create(self, db: Session, *, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data.update(kwargs)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_multi(self, db: Session, *, ids: List[int]):
        db.query(self.model).filter(self.model.id.in_(ids)).delete()
        db.commit()
