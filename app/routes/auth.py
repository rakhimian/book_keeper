from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import user as user_model
from .. import utils
from ..repository import database
from ..repository.auth.auth_repository import AuthRepository

router = APIRouter(tags=['Authentication'])
auth_repo = AuthRepository()


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(user_model.User).filter(
        user_model.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND,
            detail="Invalid credentials",
        )

    access_token = auth_repo.create_access_token(data={"user_id": user.id})

    # create a token
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
