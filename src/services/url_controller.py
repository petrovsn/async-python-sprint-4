


from models.url_record import UrlRecord
from schemas.url_record import UrlRecordCreate, UrlRecordUpdate
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel

from models.base import Base
from sqlalchemy import func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import Repository

from fastapi.encoders import jsonable_encoder

from .repository import RepositoryDB

    #id = Column(Integer, primary_key=True)
    #url_full = Column(String)
    #url_short = Column(String)
    #created_at = Column(DateTime, server_default=func.now())
    #usage_counter = Column(Integer)
    #status = Column(String)


class RepositoryURL(RepositoryDB[UrlRecord, UrlRecordCreate, UrlRecordUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: UrlRecordCreate, username: Any) -> UrlRecord:
        obj_in_data = jsonable_encoder(obj_in)
        
        
        #в качестве токена используем хэш от входящей строки
        obj_in_data["url_short"] = "shortlink"+str(hash(obj_in_data["url_full"]))
        obj_in_data["created_by"] = username

        if not username:
            obj_in_data["type"] = "public"

        db_obj = self._model(**obj_in_data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get(self, db: AsyncSession, url_short: str):
        statement = select(self._model).where(self._model.url_short == url_short)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()
    
    async def delete(self, db: AsyncSession, *, url_short: str) -> UrlRecord:
        statement = select(self._model).where(self._model.url_short == url_short)
        results = await db.execute(statement=statement)
        obj_to_del = results.scalar_one_or_none()
        obj_to_del.__setattr__("status", "deleted")
       
        await db.commit()
        await db.refresh(obj_to_del)
        return obj_to_del

urlrecord_crud = RepositoryURL(UrlRecord) 


