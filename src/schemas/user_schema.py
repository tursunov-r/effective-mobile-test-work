import re

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    model_validator,
)


class UserCreateSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=255)
    middle_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @classmethod
    @field_validator("password")
    def validate_password(cls, pwd: str):
        pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]).{8,}$'
        )
        if not pattern.match(pwd):
            raise ValueError(
                "Password must contain lowercase and uppercase letters, numbers and special characters."
            )
        return pwd

    @model_validator(mode="after")
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match.")
        return self

class UserUpdateSchema(UserCreateSchema):
    first_name: str | None = Field(min_length=1, max_length=255, default=None)
    middle_name: str | None = Field(min_length=1, max_length=255, default=None)
    last_name: str | None = Field(min_length=1, max_length=255, default=None)
    is_active: bool | None = Field(default=None)
    password: str | None = Field(min_length=8, default=None)
    confirm_password: str | None = Field(min_length=8, default=None)

    @model_validator(mode="after")
    def validate_confirm_password(self):
        # Проверяем только если оба поля заданы
        if self.password and self.confirm_password:
            if self.password != self.confirm_password:
                raise ValueError("Passwords don't match.")
        return self


class UserData(BaseModel):
    id: int
    first_name: str = Field(min_length=1, max_length=255)
    middle_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    email: EmailStr

class UserCreateResponseSchema(BaseModel):
    message: str
    data: UserData


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenData(BaseModel):
    user_id: int
    email: str
    role: str