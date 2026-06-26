from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schema import (
    UserCreateSchema,
    TokenData, UserUpdateSchema,
)
from src.repositories.user_repository import user_repository


class AdminService:
    @staticmethod
    async def get_users(session: AsyncSession, user: TokenData):
        if user.role == "admin":
            users = await user_repository.get_users_query(session=session)
            return users
        raise