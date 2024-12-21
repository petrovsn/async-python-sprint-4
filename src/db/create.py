import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from models.url_record import UrlRecord
from models.users import User
from configs.config import app_settings

async def main():
    # Замените DSN на свои значения
    DSN = app_settings.database_dsn #"postgresql+asyncpg://postgres:12345@localhost:5432/AsyncStudy"
    engine = create_async_engine(DSN, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(UrlRecord.metadata.drop_all)
        await conn.run_sync(UrlRecord.metadata.create_all)
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(User.metadata.create_all)
    
    # Дальнейшие участки кода, кроме импортов, располагайте в функции main
    # Перед закрытием приложения нужно закрыть все соединения с базой данных
    await engine.dispose()


def create_table():
    asyncio.run(main())      
