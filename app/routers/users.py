from .. import model
from .. import utils
from .. import schema
from ..database import sessionDep
from fastapi import HTTPException, status, Response, APIRouter
from sqlmodel import select

router = APIRouter(prefix="/users", tags=['Users']) #tags here helps to group these paths together in documentation!

@router.get("/", response_model=list[schema.UserPublic])
def get_users(session: sessionDep, offset: int = 0) -> list[model.User]:
    users = session.exec(select(model.User).offset(offset))
    return users

@router.get("/{id}", response_model=schema.UserPublic)
def get_user(id: int, session: sessionDep):
    user = session.get(model.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return user

@router.post("/", response_model=schema.UserPublic ,status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, session: sessionDep):

    hash_pass = utils.hash_password(user.password) #hashing password and storing it in user.password.
    user.password = hash_pass

    db_user = model.User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: sessionDep):
    user = session.get(model.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schema.UserPublic)
def update_post(id: int, user: schema.UserUpdate, session: sessionDep):
    user_db = session.get(model.User, id)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!!")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db
