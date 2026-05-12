from typing import List
from sqlalchemy import select, delete
from core.data.entities.recent_project import RecentProjectEntity
from core.models.recent_project import RecentProject
from core.repository_contracts.i_recent_project_repository import IRecentProjectRepository
from infrastructure.database.db_core import DBCore


class RecentProjectRepository(IRecentProjectRepository):
    """
    Repository for managing RecentProjectEntity entities in the database.

    Purpose: Provides high-level database operations for recent projects.
    Used In: AppDIContainer.
    """

    def __init__(self, db_core: DBCore) -> None:
        """
        Initializes the repository with a database core instance.

        Args:
            db_core: The core database manager.
        """
        self._db_core = db_core

    async def get_all(self) -> List[RecentProject]:
        """
        Retrieves all recent projects, ordered by last_opened_at descending.

        Invoked By: None.

        Returns:
            List[RecentProject]: List of all recent projects.
        """
        async with self._db_core.get_async_session() as session:
            statement = select(RecentProjectEntity).order_by(RecentProjectEntity.last_opened_at.desc())
            result = await session.execute(statement)
            entities = result.scalars().all()
            return [
                RecentProject(
                    id=e.id,
                    name=e.name,
                    path=e.path,
                    last_opened_at=e.last_opened_at
                ) for e in entities
            ]

    async def add_project(self, name: str, path: str) -> RecentProject:
        """
        Adds a new project or updates the last_opened_at of an existing one.

        Invoked By: None.

        Args:
            name: The display name of the project.
            path: The filesystem path to the project.

        Returns:
            RecentProject: The added or updated project domain model.
        """
        async with self._db_core.get_async_session() as session:
            statement = select(RecentProjectEntity).where(RecentProjectEntity.path == path)
            result = await session.execute(statement)
            existing = result.scalars().first()

            if existing:
                existing.name = name
                await session.commit()
                await session.refresh(existing)
                return RecentProject(
                    id=existing.id,
                    name=existing.name,
                    path=existing.path,
                    last_opened_at=existing.last_opened_at
                )

            new_project = RecentProjectEntity(name=name, path=path)
            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)
            return RecentProject(
                id=new_project.id,
                name=new_project.name,
                path=new_project.path,
                last_opened_at=new_project.last_opened_at
            )

    async def delete_project(self, project_id: int) -> None:
        """
        Deletes a project by its ID.

        Invoked By: None.

        Args:
            project_id: The unique identifier of the project to delete.
        """
        async with self._db_core.get_async_session() as session:
            statement = delete(RecentProjectEntity).where(RecentProjectEntity.id == project_id)
            await session.execute(statement)
            await session.commit()
