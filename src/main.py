from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.database import create_tables, create_admin
from src.api.admin_handlers import router as admin_router
from src.api.auth_handlers import router as auth_router
from src.api.user_handlers import router as user_router
from src.api.exceprion_handlers import register_exception_handlers



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_admin()
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)


routers = [admin_router, auth_router, user_router]

for router in routers:
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)