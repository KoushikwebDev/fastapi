from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import Token, UserCreate


class AuthService:
    """Service providing authentication and user registration logic."""

    def authenticate_user(
        self,
        db: Session,
        username_or_email: str,
        password: str,
    ) -> Optional[User]:
        """Authenticate a user by username/email and password."""
        user = user_repository.get_by_username_or_email(db, identifier=username_or_email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        """Register a new user with duplicate validation and password hashing."""
        if user_repository.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        if user_repository.get_by_username(db, username=user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists.",
            )

        hashed_password = get_password_hash(user_in.password)
        return user_repository.create(db, user_in=user_in, hashed_password=hashed_password)

    def create_token_for_user(self, user: User) -> Token:
        """Generate a signed JWT token response for a user."""
        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"username": user.username, "email": user.email},
        )
        return Token(access_token=access_token, token_type="bearer")


auth_service = AuthService()
