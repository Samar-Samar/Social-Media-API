from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from .config import settings

url = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(url) #use echo=True here to log all the sql commands in console that are used.

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]