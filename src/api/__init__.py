from .admin_handlers import router as admin_router
from .auth_handlers import router as auth_router
from .user_handlers import router as user_router

routers = [
    auth_router,
    admin_router,
    user_router, ]
