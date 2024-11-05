from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import Optional


# Schemas for User
class UserBase(SQLModel):
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)

class UserPublic(UserBase):
    id: int
    created_at: datetime | None = Field(default=None)

class UserCreate(UserBase):
    password: str = Field(nullable=False)

class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserLogin(SQLModel):
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)

# Schemas for Post
class PostBase(SQLModel):
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)

class PostPublic(PostBase):
    id: int
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    user_id: int
    user: UserPublic
    
class PostPublicOut(SQLModel):
    Post: PostPublic
    votes: int = 0

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Votes Schemas
class Vote(BaseModel):
    post_id: int
    vote_state: bool