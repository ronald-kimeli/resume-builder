import asyncio
import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.async_db_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# expire_on_commit=False: attributes stay readable after commit without an implicit
# (and, under asyncio, illegal) lazy refresh.
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def initialize_db(retries: int = 30, delay: float = 1.0) -> None:
    """Create tables, waiting for Postgres to accept connections."""
    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            return
        except Exception as exc:  # driver errors vary while Postgres boots
            if attempt == retries:
                raise
            logger.warning("Database not ready (%s), retry %s/%s", exc, attempt, retries)
            await asyncio.sleep(delay)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
