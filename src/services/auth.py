from typing import Optional
from schemas import users as user_schema
from db.db import async_session
from services.users import users_crud
from fastapi import Request, HTTPException, status

#проверка юзера на авторизацию
async def get_auth(request: Request):
    try:
        
        headers = request.headers
        login = headers.get("login")
        password = headers.get("password")
        async with async_session() as session:
            user_verification = await users_crud.verify(session, login, password)
            if user_verification: return login

    except Exception as e:
        pass
    return None