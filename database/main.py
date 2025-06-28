from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


sql_db_url = 'sqlite:///./TaskManager.db' # Строка подключения к базе данных SQLite.

engine = create_engine(sql_db_url) # Основной интерфейс к базе данных.

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine) # Фабрика для создания сессий БД.

Base = declarative_base() # Базовый класс для всех моделей SQLAlchemy.