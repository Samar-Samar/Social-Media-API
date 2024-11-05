from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from pydantic import EmailStr
from typing import List

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})

    posts : List["Post"] = Relationship(back_populates="user", cascade_delete=True)

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime | None = Field(default=None, nullable=True, sa_column_kwargs={"onupdate": func.now()})
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE",nullable=False)

    user : User | None = Relationship(back_populates="posts")

class Vote(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True, ondelete="CASCADE")
    post_id: int = Field(foreign_key="post.id",  primary_key=True, ondelete="CASCADE")