from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from src.core.database import create_tables, create_admin
from src.api.admin_handlers import router as admin_router
from src.api.auth_handlers import router as auth_router
from src.api.user_handlers import router as user_router
from src.api.exceprion_handlers import register_exception_handlers
from src.core.limiter import limiter
from src.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_admin()
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

routers = [admin_router, auth_router, user_router]

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
