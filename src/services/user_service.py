from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import user_repository
from src.schemas.user_schemas import (
    TokenData,
    UserCreateSchema,
    UserLoginSchema,
    UserUpdateSchema,
)
from src.services.logger import log_service


class UserService:
    @staticmethod
    async def create_user(user: UserCreateSchema, session: AsyncSession):
        create_user = await user_repository.create_user_query(
            user=user, session=session
        )
        log_service.info("create new user: ", user=user.email)
        return create_user

    @staticmethod
    async def update_user(
        token: TokenData, user: UserUpdateSchema, session: AsyncSession
    ):
        update_user = await user_repository.update_user_query(
            token=token, user=user, session=session
        )
        log_service.info("update self profile: ", user=token.email)
        return update_user

    @staticmethod
    async def delete_user(
        token: TokenData, user: UserLoginSchema, session: AsyncSession
    ):
        delete_user = await user_repository.delete_user_query(
            token=token, user=user, session=session
        )
        log_service.info("delete self profile: ", user=token.email)
        return delete_user


user_service = UserService()
