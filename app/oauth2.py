import jwt
from jwt import PyJWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlmodel import select
from . import model, database, schema
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_Encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_Encode.update({"exp": expire})

    token = jwt.encode(to_Encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("userID")

        if id is None:
            raise credentials_exception
        
        
        token_data = schema.TokenData(user_id=id)
    
    except PyJWTError as e:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: database.sessionDep):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials!', headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    stmt = select(model.User).where(model.User.id == token_data.user_id)
    user = session.exec(stmt).first()

    return user
