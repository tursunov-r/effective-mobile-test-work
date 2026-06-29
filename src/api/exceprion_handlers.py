from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.auth_exceptions import (
    Forbidden,
    InvalidCredentials,
    Unauthorized,
)
from src.exceptions.user_exceptions import UserAlreadyExists, UserNotFound
from src.services.logger import log_service


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Unauthorized)
    async def jwt_error_handler(
        request: Request,
        exc: Unauthorized,
    ):
        log_service.error(
            "try login",
            error=exc,
        )
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(Forbidden)
    async def permission_error_handler(
        request: Request,
        exc: Forbidden,
    ):
        log_service.error("permission error", error=exc)
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyExists)
    async def email_already_exists_handler(
        request: Request,
        exc: UserAlreadyExists,
    ):
        log_service.error("try to create user", error=str(exc))
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentials,
    ):
        log_service.error("try to create user", error=str(exc))
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFound,
    ):
        log_service.error("try to create user", error=str(exc))
        return JSONResponse(status_code=404, content={"detail": str(exc)})
