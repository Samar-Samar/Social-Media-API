from fastapi import HTTPException, status, Response, APIRouter, Depends
from sqlmodel import select
from .. import schema, model, oauth2
from ..database import sessionDep
from typing import Annotated

router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, session: sessionDep, curr_user: Annotated[model.User, Depends(oauth2.get_current_user)]):
    
    stmt_post = select(model.Post).where(model.Post.id == vote.post_id)
    found_post = session.exec(stmt_post).first()

    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="given post was not found!!")

    stmt_vote = select(model.Vote).where(model.Vote.user_id == curr_user.id, model.Vote.post_id == vote.post_id)
    found_vote = session.exec(stmt_vote).first()
    
    if(vote.vote_state):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {curr_user.id} has already voted on the post {vote.post_id}")
        new_vote = model.Vote(post_id= vote.post_id, user_id= curr_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        
        session.delete(found_vote)
        session.commit()

        return {"message": "successfully deleted vote!"}