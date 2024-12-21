




import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse
from configs.config import app_settings
from configs.logger import LOGGING

from services.blacklist import check_allowed_ip
from api.v1 import url_record, users
from db.create import create_table, main

#create_table()
#quit()

app = FastAPI(
    # Название проекта. Оно будет отображаться в документации
    title=app_settings.app_title,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    # Можно сразу сделать небольшую оптимизацию сервиса и заменить
    # стандартный JSON-сериализатор на более шуструю версию, 
    # написанную на Rust
    default_response_class=ORJSONResponse,
    dependencies=[Depends(check_allowed_ip)]
)

app.include_router(url_record.router, prefix='')
app.include_router(users.router, prefix='/users')
if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8080 --app-dir src`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host="0.0.0.0",
        port=8000,
    ) 