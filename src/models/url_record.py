from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship, declarative_base

from .base import Base





class UrlRecord(Base):
    # Имя таблицы в базе данных
    __tablename__ = "UrlRecord"

    id = Column(Integer, primary_key=True)
    url_full = Column(String, unique=True)
    url_short = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String, default = None)
    usage_counter = Column(Integer, default=0)
    status = Column(String, default="active")
    type = Column(String, default = "public")

    # Значение `eager_defaults` указывает ORM немедленно получать значение
    # сгенерированных сервером значений по умолчанию для INSERT или UPDATE.
    __mapper_args__ = {"eager_defaults": True}

    
    # Чтобы сделать консольный вывод более информативным, добавим __repr__
    def __repr__(self):
        return f"UrlRecord: {self.url_full}"