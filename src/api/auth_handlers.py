from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.limiter import limiter
from src.schemas.user_schemas import UserLoginSchema
from src.core.db_connect import get_session
from src.services.profile_service import profile_service

router = APIRouter(prefix="/api/v1/profiles", tags=["profile v1"])


@router.post("/")
@limiter.limit("1/minute")
async def login(
    user: UserLoginSchema,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    result = await profile_service.login_user(
        user=user, response=response, session=session
    )
    return result


@router.post("/logout")
@limiter.limit("1/minute")
async def logout(
    request: Request,
    response: Response,
):
    await profile_service.logout_user(response)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response