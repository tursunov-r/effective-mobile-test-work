from fastapi import Request, FastAPI

from fastapi.responses import JSONResponse

from src.exceptions.auth_exceptions import Unauthorized, Forbidden, InvalidCredentials
from src.exceptions.user_exceptions import UserNotFound, UserAlreadyExists


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Unauthorized)
    async def jwt_error_handler(
            request: Request,
            exc: Unauthorized,
    ):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(Forbidden)
    async def permission_error_handler(
            request: Request,
            exc: Forbidden,
    ):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyExists)
    async def email_already_exists_handler(
            request: Request,
            exc: UserAlreadyExists,
    ):
        return JSONResponse(
            status_code=400, content={"detail": str(exc)}
        )

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(
            request: Request,
            exc: InvalidCredentials,
    ):
        return JSONResponse(
            status_code=401, content={"detail": str(exc)}
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(
            request: Request,
            exc: UserNotFound,
    ):
        return JSONResponse(
            status_code=404, content={"detail": str(exc)}
        )
