from typing import AsyncGenerator
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker


# для локалки поменять порт на 5436 !!! ДЛЯ ДОКЕРА 5432
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DB_URL)

Base: DeclarativeMeta = declarative_base()
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def init_db():
    Base.metadata.create_all(bind=engine)