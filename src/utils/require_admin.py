from fastapi import Depends

from src.exceptions.auth_exceptions import Forbidden
from src.schemas.user_schemas import TokenData
from src.utils.auth import get_current_user


def require_admin(user: TokenData = Depends(get_current_user)):
    """Функция для проверки прав"""
    if user.role == "admin":
        return user
    raise Forbidden("You are not allowed to perform this action")
