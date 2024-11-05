from .. import model
from .. import oauth2
from .. import schema
from ..database import sessionDep
from sqlmodel import select, func
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status, Response, APIRouter, Depends
from typing import Annotated, Optional

router = APIRouter(prefix="/posts", tags=['Posts']) #tags here helps to group these paths together in documentation!

@router.get("/", response_model=list[schema.PostPublicOut])
def get_posts(session: sessionDep, curr_user: Annotated[model.User, Depends(oauth2.get_current_user)], skip: int = 0, limit: int = 10, search: Optional[str] = "" ):

    stmt = select(model.Post, func.count(model.Vote.post_id).label("votes")).outerjoin(model.Vote, model.Vote.post_id == model.Post.id).filter(model.Post.title.contains(search)).group_by(model.Post.id).offset(skip).limit(limit)
    results = session.exec(stmt).all()

    return results

@router.get("/{id}", response_model=schema.PostPublicOut)
def get_posts(id: int, session: sessionDep, curr_user: Annotated[model.User, Depends(oauth2.get_current_user)]):
    
    stmt = select(model.Post, func.count(model.Vote.post_id).label("votes")).outerjoin(model.Vote, model.Vote.post_id == model.Post.id).where(model.Post.id == id).group_by(model.Post.id)
    post = session.exec(stmt).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    
    return post

@router.post("/", response_model=schema.PostPublic ,status_code=status.HTTP_201_CREATED)
def create_post(post: schema.PostCreate, session: sessionDep, curr_user: Annotated[model.User, Depends(oauth2.get_current_user)]):
    post_data = post.model_dump()
    post_data["user_id"] = curr_user.id
    db_post = model.Post.model_validate(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: sessionDep, curr_user: Annotated[model.User, Depends(oauth2.get_current_user)]):
    post = session.get(model.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action!")
    
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=schema.PostPublic)
def update_post(id: int, post: schema.PostUpdate, session: sessionDep, curr_user: Annotated[model.User, Depends(oauth2.get_current_user)]):
    post_db = session.get(model.Post, id)
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!!")
    if post_db.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action!")
    
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db
