from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.schemas import auth as auth_schema
from app.models import user as user_model
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db
from app.repository.auth.abstract_auth_repository import AbstractAuthRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorythm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class AuthRepository(AbstractAuthRepository):
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception: HTTPException) -> auth_schema.TokenData:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("user_id")

            if user_id is None:
                raise credentials_exception

            token_data = auth_schema.TokenData(id=user_id)

        except JWTError:
            raise credentials_exception

        return token_data


