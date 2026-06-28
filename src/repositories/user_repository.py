from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.models.user_model import UserModel
from src.schemas.admin_schemas import AdminUserCreateSchema, AdminUserUpdateSchema
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserUpdateSchema, TokenData,
)
from src.utils.auth import hash_password, verify_password


class UserRepository:
    @staticmethod
    async def create_user_query(user: UserCreateSchema | AdminUserCreateSchema, session: AsyncSession):
        existing = await session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        if existing.scalar_one_or_none():
            raise ValueError("User already exists")

        hash_pwd = hash_password(user.password)
        query = UserModel(
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            email=str(user.email).lower(),
            password=hash_pwd,
            role="user",  # дефолтная роль
        )

        if isinstance(user, AdminUserCreateSchema):
            query.role = user.role if user.role else "user"

        session.add(query)
        await session.flush()
        return query



    @staticmethod
    async def get_users_query(session: AsyncSession):
        result = await session.execute(
            select(UserModel)
        )
        users = result.scalars().all()
        if users:
            return users
        raise

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession):
        user = await session.execute(select(UserModel).where(UserModel.id == user_id))
        result = user.scalar_one_or_none()
        if result:
            return result
        raise

    @staticmethod
    async def get_profile(token: TokenData, session: AsyncSession):
        profile = await session.execute(select(UserModel).where(UserModel.email == token.email))
        result = profile.scalar_one_or_none()
        if result:
            return result
        raise

    @staticmethod
    async def update_user_query(token: TokenData, user: UserUpdateSchema | AdminUserUpdateSchema,
                                session: AsyncSession):
        if isinstance(user, AdminUserUpdateSchema):
            # если запрос на обновление пользователя от админа (user_id из схемы)
            query = await session.execute(select(UserModel).where(UserModel.id == user.user_id))
        else:
            # иначе получаем id пользователя из JWT, так как api пользователя не может указывать произвольный user_id
            query = await session.execute(select(UserModel).where(UserModel.id == token.user_id))

        result = query.scalar_one_or_none()
        if user.first_name:
            result.first_name = user.first_name.title()
        if user.middle_name:
            result.middle_name = user.middle_name.title()
        if user.last_name:
            result.last_name = user.last_name.title()
        if user.password and user.confirm_password:
            result.password = hash_password(user.password)
        if isinstance(user, AdminUserUpdateSchema) and user.role:
            # если пользователя обновляет админ, можно обновить роль.
            result.role = user.role
        session.add(result)
        return result

    @staticmethod
    async def delete_user_query(token: TokenData, user: UserLoginSchema, session: AsyncSession):

        query = await session.execute(
            select(UserModel).where(UserModel.id == token.user_id)
        )
        result = query.scalar_one_or_none()
        verify = verify_password(user.password, str(result.password))
        if result.email == user.email and verify:
            print("password match")
            result.is_active = False
            session.add(result)
            return result
        raise

    @staticmethod
    async def delete_user_by_id(user_id: int, session: AsyncSession):
        query = await session.execute(select(UserModel).where(UserModel.id == user_id))
        result = query.scalar_one_or_none()
        if result:
            result.is_active = False
            session.add(result)
            return result
        raise

    @staticmethod
    async def create_admin_query(session: AsyncSession):
        hash_pwd = hash_password(settings.admin_password)

        result = await session.execute(
            select(UserModel).where(UserModel.email == settings.admin_email)
        )
        existing = result.scalar_one_or_none()

        if existing:
            return

        create_admin = UserModel(
            email=settings.admin_email,
            password=hash_pwd,
            first_name=settings.admin_first_name,
            middle_name=settings.admin_middle_name,
            last_name=settings.admin_last_name,
            role="admin"
        )

        session.add(create_admin)
        print("Admin created")


user_repository = UserRepository()
