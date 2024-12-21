from sqlalchemy import Column, DateTime, func, Integer, String

from .base import Base





class User(Base):
    # Имя таблицы в базе данных
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)

    #в случае не учебной задачи, разумеется, хранить пароль в открытом виде - плохая идея 
    #и стоит писать отдельный сервис авторизации для вычисления хэшей, проверки паролей 
    #и выдачи токенов
    password = Column(String)

    # Значение `eager_defaults` указывает ORM немедленно получать значение
    # сгенерированных сервером значений по умолчанию для INSERT или UPDATE.
    __mapper_args__ = {"eager_defaults": True}

    # Чтобы сделать консольный вывод более информативным, добавим __repr__
    def __repr__(self):
        return f"User {self.login}"