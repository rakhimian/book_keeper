"""
Модуль описывает репозиторий, работающий c PostgreSql
"""

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models import user as user_model
from app.repository.auth.auth_repository import AuthRepository
from app.repository.database import get_db
from app.repository.user.abstract_user_repository import AbstractUserRepository, oauth2_scheme

auth_repo = AuthRepository()


class UserRepository(AbstractUserRepository):
    """
        Репозиторий, работающий с базой данных PostgreSQL.
    """

    def get_current_user(self, token: str = Depends(oauth2_scheme),
                         db: Session = Depends(get_db)) -> user_model.User | None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer",
            }
        )

        token_data = auth_repo.verify_access_token(token, credentials_exception)

        current_user = db.query(user_model.User).filter(user_model.User.id == token_data.id).first()

        return current_user

