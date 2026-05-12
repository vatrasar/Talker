import pkgutil
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import DATABASE_URL
from core.data.entities.entity_base import BaseEntity


class DBCore:
    """
    Core database configuration and session management.

    Purpose: Manages SQLAlchemy async engine, session factory, and provides
    context-managed asynchronous database sessions.
    Used In: AppDIContainer, repositories, and services requiring database access.
    """

    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        self.session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    async def init_db_schema(self) -> None:
        """
        Initializes the database schema by importing all entities and creating tables.

        Used In: AppDIContainer during application startup.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseEntity.metadata.create_all)
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides an asynchronous transactional scope around a series of operations.

        Yields:
            AsyncSession: A SQLAlchemy async session instance.
        
        Used In: Repositories and use cases for database transactions.
        """
        session = self.session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback() 
            raise e
        finally:
            await session.close()

    

