from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import users as user_schema
from db.db import get_session
from services.users import users_crud
from services.url_controller import urlrecord_crud
from services.utils import execution_controller
from services.auth import get_auth
# Объект router, в котором регистрируем обработчики
router = APIRouter()




#создание записи
@execution_controller
@router.post(
    "/create", status_code=status.HTTP_200_OK  #response_model=url_schema.UrlRecord, 
)
async def create_user(
    *,
    db: AsyncSession = Depends(get_session),
    entity_in: user_schema.UserCreate,
) -> Any:
    # create item by params
    entity = await users_crud.create(db=db, obj_in=entity_in)
    return entity


#создание записи
@execution_controller
@router.get(
    "/status", status_code=status.HTTP_200_OK  #response_model=url_schema.UrlRecord, 
)
async def get_users_urls(
    *,
    db: AsyncSession = Depends(get_session),
    user_login = Depends(get_auth), login:str = Header(None), password :str = Header(None), 
) -> Any:
    if not user_login: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        
    result = []
    all_urls = await urlrecord_crud.get_multi(db=db)
    for url in all_urls:
        if url.created_by == user_login:
            result.append(url)
    return result

