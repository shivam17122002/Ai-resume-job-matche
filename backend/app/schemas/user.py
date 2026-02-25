from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_length_for_bcrypt(cls, value: str) -> str:
        # bcrypt only supports passwords up to 72 bytes.
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password is too long. Use at most 72 bytes.")
        return value


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
