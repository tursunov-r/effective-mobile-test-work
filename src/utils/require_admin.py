from src.exceptions.auth_exceptions import Forbidden
from src.schemas.user_schemas import TokenData


def require_admin(user: TokenData):
    """Функция для проверки прав"""
    if user.role == "admin":
        return user
    raise Forbidden("You are not allowed to perform this action")
