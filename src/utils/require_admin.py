from src.schemas.user_schemas import TokenData


def require_admin(user: TokenData):
    """Функция для проверки прав"""
    if user.role == "admin":
        return user
    raise
