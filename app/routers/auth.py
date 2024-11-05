from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import select
from ..database import sessionDep
from .. import model
from .. import utils
from .. import oauth2
from .. import schema

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schema.Token)
def login(user_credentials : Annotated[OAuth2PasswordRequestForm, Depends()], session: sessionDep):
    stmt = select(model.User).where(model.User.email == user_credentials.username)
    user = session.exec(stmt).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    
    if not utils.pass_verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data= {"userID": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}