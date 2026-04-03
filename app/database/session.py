from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

engine = create_async_engine(
    # database type/dialect and file name
    url=settings.POSTGRES_URL,
    # Log sql queries
    echo=True,
)

async def create_db_tables():
    async with engine.begin() as connection:
        from app.schemas import Shipment  # noqa: F401
        await connection.run_sync(SQLModel.metadata.create_all(bind=engine))

async def get_session():
    async_session = sessionmaker (
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]