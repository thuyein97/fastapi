from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import databasetest, schema, model, utils, oauth

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(databasetest.get_db)):

    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth.create_access_token(data = {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}