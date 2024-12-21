


from models.users import User
from schemas.users import UserCreate, UserUpdate
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


class RepositoryUsers(RepositoryDB[User, UserCreate, UserUpdate]):  
    async def verify(self, db: AsyncSession, login: str, password: str):
        statement = select(self._model).where(self._model.login == login, self._model.password == password)
        results = await db.execute(statement=statement)
        user = results.scalar_one_or_none()
        if user: return True
        return False

users_crud = RepositoryUsers(User) 


