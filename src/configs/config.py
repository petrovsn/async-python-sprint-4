import os
from logging import config as logging_config

from .logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
#PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
#PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
#PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

# Корень проекта
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from pydantic import BaseSettings, PostgresDsn
...

class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


app_settings = AppSettings() 