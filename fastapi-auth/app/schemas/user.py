from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


# Base User Schema
class UserBase(BaseModel):
    email: str = Field(..., pattern=EMAIL_PATTERN, description="User email address", examples=["user@example.com"])
    username: str = Field(..., min_length=3, max_length=50, description="Username", examples=["johndoe"])
    full_name: Optional[str] = Field(default=None, max_length=100, description="Full name", examples=["John Doe"])
    is_active: Optional[bool] = Field(default=True, description="Account active status")


# Schema for User Registration / Creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128, description="User password", examples=["securepassword123"])


# Schema for Updating User
class UserUpdate(BaseModel):
    email: Optional[str] = Field(default=None, pattern=EMAIL_PATTERN, description="User email address")
    username: Optional[str] = Field(default=None, min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(default=None, max_length=100, description="Full name")
    password: Optional[str] = Field(default=None, min_length=8, max_length=128, description="New password")
    is_active: Optional[bool] = None


# Schema for User Response
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


# JWT Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


# Login Schema (JSON payload alternative to OAuth2 form)
class LoginRequest(BaseModel):
    username_or_email: str = Field(..., description="Username or email", examples=["johndoe"])
    password: str = Field(..., description="User password", examples=["securepassword123"])
