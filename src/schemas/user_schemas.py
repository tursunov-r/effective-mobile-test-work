import re

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)
from src.schemas.mixins import PasswordMixin


class UserCreateSchema(PasswordMixin):
    first_name: str = Field(min_length=1, max_length=255)
    middle_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class UserUpdateSchema(UserCreateSchema):
    first_name: str | None = Field(min_length=1, max_length=255, default=None)
    middle_name: str | None = Field(min_length=1, max_length=255, default=None)
    last_name: str | None = Field(min_length=1, max_length=255, default=None)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(min_length=8, default=None)
    confirm_password: str | None = Field(min_length=8, default=None)


class UserDataResponseSchema(BaseModel):
    id: int
    first_name: str = Field(min_length=1, max_length=255)
    middle_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    email: EmailStr


class UserCreateResponseSchema(BaseModel):
    message: str
    data: UserDataResponseSchema


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenData(BaseModel):
    user_id: int
    email: str
    role: str