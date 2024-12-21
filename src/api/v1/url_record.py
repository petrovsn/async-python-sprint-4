from fastapi import APIRouter, Header
from fastapi.responses import HTMLResponse
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from  schemas import url_record as url_schema
from schemas import users as user_schema
from db.db import get_session, async_session
from services.url_controller import urlrecord_crud
from services.users import users_crud
from services.utils import execution_controller
from services.auth import get_auth
# Объект router, в котором регистрируем обработчики
router = APIRouter()

@execution_controller
@router.get("/test/ep")
async def get_url_full() -> Any:
    return "ok"


#создание записи
@execution_controller
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session), url_data: url_schema.UrlRecordCreate, 
                           login:Optional[str] = Header(None), password :Optional[str] = Header(None), user_login = Depends(get_auth)):

    try:
        entity = await urlrecord_crud.create(db=db, obj_in=url_data, username=user_login)
        return entity
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, headers = {"message":repr(e)}) 


#загрузка батча ссылок
@execution_controller
@router.post(
    "/shorten", status_code=status.HTTP_201_CREATED  #response_model=url_schema.UrlRecord, 
)
async def create_short_url_batch(
    *,
    db: AsyncSession = Depends(get_session),
    entity_in_list: List[url_schema.UrlRecordCreate], login:Optional[str] = Header(None), password :Optional[str] = Header(None), user_login = Depends(get_auth)):
    result = []
    for entity_in in entity_in_list:
        try:
            entity = await urlrecord_crud.create(db=db, obj_in=entity_in, username=user_login)
            result.append(entity)
        except Exception as e:
            pass
    return result


#переадресация по короткой ссылке
@execution_controller
@router.get("/{url_short}")
async def get_url_full(
    *,
    db: AsyncSession = Depends(get_session),
    url_short: str, login:Optional[str] = Header(None), password :Optional[str] = Header(None), user_login = Depends(get_auth)
) -> Any:
    """
    Get by ID.
    """
    url_record = await urlrecord_crud.get(db=db, url_short=url_short)
    if not url_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    #если ссылка была удалена
    if url_record.status == "deleted":
        raise HTTPException(status_code=status.HTTP_410_GONE)
    
    #если пользователь не имеет к ней доступа
    if url_record.type == "private":
        if url_record.created_by != user_login:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
    url_record = await urlrecord_crud.update(db = db, db_obj=url_record, obj_in={"usage_counter":url_record.usage_counter+1})
    
    return HTMLResponse(None, status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location":url_record.url_full})



#редактирование ссылки
@execution_controller
@router.put("/{url_short}")
async def update_url(
    *,
    db: AsyncSession = Depends(get_session),
    url: url_schema.UrlRecordUpdate,
    user_login = Depends(get_auth), login:Optional[str] = Header(None), password :Optional[str] = Header(None), 
    url_short: str, 
) -> Any:

    #запрет использования без авторизации
    if not user_login: return HTMLResponse(None, status_code=status.HTTP_403_FORBIDDEN)

    url_record = await urlrecord_crud.get(db=db, url_short=url_short)
    if not url_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    #если ссылка приватная, то без авторизации использовать невозможно
    if url_record.type == "private":
        if url_record.created_by != user_login:
            return HTMLResponse(None, status_code=status.HTTP_403_FORBIDDEN)
    
    url_record = await urlrecord_crud.update(db = db, db_obj=url_record, obj_in={"type":url.type})    
    return url_record


from fastapi.responses import HTMLResponse
#информация о короткой ссылке
@execution_controller
@router.get("/{url_short}/info")
async def get_url_full(
    *,
    db: AsyncSession = Depends(get_session),
    url_short: str ,login:Optional[str] = Header(None), password :Optional[str] = Header(None), user_login = Depends(get_auth)
) -> Any:
    """
    Get by ID.
    """
    url_record = await urlrecord_crud.get(db=db, url_short=url_short)
    if not url_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return url_record


#переадресация по короткой ссылке
@execution_controller
@router.delete("/{url_short}")
async def delete_short_url(
    *,
    db: AsyncSession = Depends(get_session),
    url_short: str, login:Optional[str] = Header(None), password :Optional[str] = Header(None), user_login = Depends(get_auth)
) -> Any:
    """
    Get by ID.
    """
    url_record = await urlrecord_crud.get(db=db, url_short=url_short)
    if not url_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    url_record = await urlrecord_crud.delete(db = db, url_short=url_short)
    # get entity from db
    return url_record


#переадресация по короткой ссылке
@execution_controller
@router.get("/utils/ping")
async def ping_db(db: AsyncSession = Depends(get_session)) -> Any:
    """
    Get by ID.
    """
    try:
        result = await db.connection()
        return True
    except Exception as e:
        return False