from typing import Optional, Sequence
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """Repository handling database operations for the User entity."""

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Fetch a single user by primary key ID."""
        return db.get(User, user_id)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Fetch a single user by email address."""
        statement = select(User).where(User.email == email)
        return db.execute(statement).scalar_one_or_none()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Fetch a single user by username."""
        statement = select(User).where(User.username == username)
        return db.execute(statement).scalar_one_or_none()

    def get_by_username_or_email(self, db: Session, identifier: str) -> Optional[User]:
        """Fetch a user matching either username or email."""
        statement = select(User).where(
            or_(User.username == identifier, User.email == identifier)
        )
        return db.execute(statement).scalar_one_or_none()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
        """Fetch multiple users with pagination."""
        statement = select(User).offset(skip).limit(limit)
        return db.execute(statement).scalars().all()

    def create(self, db: Session, user_in: UserCreate, hashed_password: str) -> User:
        """Create and persist a new user record."""
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            is_active=user_in.is_active if user_in.is_active is not None else True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self,
        db: Session,
        db_user: User,
        user_in: UserUpdate,
        hashed_password: Optional[str] = None,
    ) -> User:
        """Update existing user fields."""
        update_data = user_in.model_dump(exclude_unset=True, exclude={"password"})
        for field, value in update_data.items():
            setattr(db_user, field, value)

        if hashed_password is not None:
            db_user.hashed_password = hashed_password

        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(self, db: Session, db_user: User) -> None:
        """Delete a user record from the database."""
        db.delete(db_user)
        db.commit()


user_repository = UserRepository()
