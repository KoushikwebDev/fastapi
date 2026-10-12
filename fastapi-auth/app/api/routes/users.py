from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.db.session import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
def read_current_user(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """Retrieve details of the currently authenticated user."""
    return UserResponse.model_validate(current_user)


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """Update profile information for the authenticated user."""
    # Check if new email is already taken by someone else
    if user_in.email and user_in.email != current_user.email:
        existing = user_repository.get_by_email(db, email=user_in.email)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use.",
            )

    # Check if new username is already taken by someone else
    if user_in.username and user_in.username != current_user.username:
        existing = user_repository.get_by_username(db, username=user_in.username)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use.",
            )

    hashed_password = (
        get_password_hash(user_in.password) if user_in.password else None
    )

    updated_user = user_repository.update(
        db=db,
        db_user=current_user,
        user_in=user_in,
        hashed_password=hashed_password,
    )
    return UserResponse.model_validate(updated_user)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List users",
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> Sequence[UserResponse]:
    """Retrieve all users with pagination (requires active login)."""
    users = user_repository.get_multi(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> UserResponse:
    """Retrieve specific user details by ID (requires active login)."""
    user = user_repository.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return UserResponse.model_validate(user)
