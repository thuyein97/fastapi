from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
import schema, databasetest, model, oauth
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(databasetest.get_db), current_user: int = 
         Depends(oauth.get_current_user)):
    
    post_query = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if post_query:
        vote_query = db.query(model.Vote).filter(vote.post_id == model.Vote.post_id, model.Vote.user_id == current_user.id)
        found_vote = vote_query.first()
        if (vote.dir == 1):
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}
        else: 
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} doesn't exit")
        
    