from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
    TokenData, UserUpdateSchema,
)
from src.repositories.user_repository import user_repository


class UserService:
    @staticmethod
    async def create_user(user: UserCreateSchema, session: AsyncSession):
        create_user = await user_repository.create_user_query(
            user=user, session=session
        )
        if create_user:
            return create_user
        raise

    @staticmethod
    async def get_profile(token: TokenData, session: AsyncSession):
        profile = await user_repository.get_profile_query(token=token, session=session)
        return profile

    @staticmethod
    async def update_user(token: TokenData, user: UserUpdateSchema, session: AsyncSession):
        update_user = await user_repository.update_user_query(token=token, user=user, session=session)
        return update_user

    @staticmethod
    async def delete_user(token: TokenData, user: UserLoginSchema, session: AsyncSession):
        delete_user = await user_repository.delete_user_query(
            token=token, user=user, session=session
        )
        if delete_user:
            return Response(status_code=204)
        raise


user_service = UserService()