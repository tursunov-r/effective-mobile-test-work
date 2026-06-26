from pydantic import Field

from src.schemas.user_schemas import UserCreateSchema, UserUpdateSchema, UserDataResponseSchema, UserCreateResponseSchema


class AdminUserCreateSchema(UserCreateSchema):
    role: str = Field(min_length=1, max_length=255, default="user")


class AdminUserUpdateSchema(UserUpdateSchema):
    user_id: int = Field(ge=1)
    role: str | None = Field(min_length=1, max_length=255, default=None)


class AdminUserDataResponseSchema(UserDataResponseSchema):
    role: str


class AdminUserCreateResponseSchema(UserCreateResponseSchema):
    data: AdminUserDataResponseSchema