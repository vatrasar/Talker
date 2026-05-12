import pkgutil
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import DATABASE_URL
from core.data.entities.entity_base import EntityBase


class DBCore:
    """
    Core database configuration and session management.

    Purpose: Manages SQLAlchemy engine, session factory, and provides
    context-managed database sessions.
    Used In: AppDIContainer, repositories, and services requiring database access.
    """

    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        self.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def init_db_schema(self) -> None:
        """
        Initializes the database schema by importing all entities and creating tables.

        Used In: AppDIContainer during application startup.
        """
        EntityBase.metadata.create_all(bind=self.engine)
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Provides a transactional scope around a series of operations.

        Yields:
            Session: A SQLAlchemy session instance.
        
        Used In: Repositories and use cases for database transactions.
        """
        session = self.session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback() 
            raise e
        finally:
            session.close()

    

