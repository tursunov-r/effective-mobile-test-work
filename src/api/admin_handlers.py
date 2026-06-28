from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_connect import get_session
from src.repositories.user_repository import user_repository
from src.schemas.admin_schemas import AdminUserDataResponseSchema, AdminUserCreateSchema, AdminUserCreateResponseSchema, \
    AdminUserUpdateSchema
from src.schemas.user_schemas import TokenData
from src.services.admin_service import admin_service
from src.utils.auth import get_current_user
from src.utils.require_admin import require_admin

router = APIRouter(prefix="/api/v1/admin_handlers/users", tags=["admin"])


@router.post("/", response_model=AdminUserCreateResponseSchema, status_code=201)
async def create_user(user: AdminUserCreateSchema, session: AsyncSession = Depends(get_session),
                      token: TokenData = Depends(get_current_user)):
    result = await admin_service.create_user(user=user, session=session, token=token)
    return {"message": "create success", "data": result}


@router.get("/", response_model=list[AdminUserDataResponseSchema])
async def get_users(
        session: AsyncSession = Depends(get_session),
        token: TokenData = Depends(get_current_user),
):
    users = await admin_service.get_users(session=session, token=token)
    return users


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session),
                         token: TokenData = Depends(get_current_user)):
    result = await user_repository.get_user_by_id(user_id=user_id, session=session)
    return result


@router.patch("/", response_model=AdminUserCreateResponseSchema)
async def update_user(user: AdminUserUpdateSchema, session: AsyncSession = Depends(get_session),
                      token: TokenData = Depends(get_current_user)):
    updated_user = await admin_service.update_user(user=user, session=session, token=token)
    return {"message": "update success", "data": updated_user}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    await admin_service.delete_user(user_id=user_id,session=session)
    return status.HTTP_204_NO_CONTENT
