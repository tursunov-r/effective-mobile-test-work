from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.db_connect import get_session
from src.core.limiter import limiter
from src.schemas.user_schemas import (
    TokenData,
    UserCreateResponseSchema,
    UserCreateSchema,
    UserDataResponseSchema,
    UserLoginSchema,
    UserUpdateSchema,
)
from src.services.profile_service import profile_service
from src.services.user_service import user_service
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["user v1"])


@router.post("/", response_model=UserCreateResponseSchema)
@limiter.limit("5/minute")
async def create_user(
    user: UserCreateSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Регистрация нового пользователя"""
    new_user = await user_service.create_user(user=user, session=session)
    return {"message": "Created", "data": new_user}


@router.get("/me", response_model=UserDataResponseSchema)
@limiter.limit("5/minute")
async def get_profile(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_token: TokenData = Depends(get_current_user),
):
    """Получить данные своего профиля"""
    profile = await profile_service.get_user_profile(
        session=session, user=user_token
    )
    return profile


@router.patch("/me", response_model=UserDataResponseSchema)
@limiter.limit("5/minute")
async def update_profile(
    request: Request,
    user: UserUpdateSchema,
    user_token: TokenData = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Обновить свой профиль"""
    updated_profile = await user_service.update_user(
        token=user_token, user=user, session=session
    )
    return updated_profile


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_user(
    request: Request,
    user: UserLoginSchema,
    session: AsyncSession = Depends(get_session),
    token: TokenData = Depends(get_current_user),
):
    """Удалить свой аккаунт (заблокировать)"""
    await user_service.delete_user(user=user, session=session, token=token)
    return None
