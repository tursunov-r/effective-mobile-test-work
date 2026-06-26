from src.core.db_connect import engine
from src.models.base_model import (
    Base,
)
from src.core.db_connect import async_session
from src.repositories.user_repository import user_repository


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created")

async def create_admin():
    async with async_session() as session:
        await user_repository.create_admin_query(session)
        await session.commit()
        print("Admin created")
