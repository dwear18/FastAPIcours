from sqlalchemy.orm import Session
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет ассинхронную сессию SQLAlcemy для работы с базой данных
    PostgresSQL.
    """
    async with async_session_maker() as session:
        yield session