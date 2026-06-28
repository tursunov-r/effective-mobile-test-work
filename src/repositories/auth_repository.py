from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_model import UserModel
from src.schemas.user_schemas import (
    UserLoginSchema,
    TokenData,
)
from src.utils.auth import verify_password


class AuthRepository:
    @staticmethod
    async def login_user_query(user: UserLoginSchema, session: AsyncSession):
        query = await session.execute(
            select(UserModel).where(
                and_(
                    UserModel.email == user.email,
                    UserModel.is_active.is_(True),
                )
            )
        )
        result = query.scalar_one_or_none()
        if result:
            verified = verify_password(user.password, result.password)
            if verified:
                return result
        raise

    @staticmethod
    async def get_profile_query(session: AsyncSession, user: TokenData):
        result = await session.execute(
            select(UserModel).where(
                and_(
                    UserModel.id == user.user_id, UserModel.email == user.email
                )
            )
        )
        user = result.scalar_one_or_none()
        if user:
            return user
        raise


auth_repository = AuthRepository()