from typing import List, Optional
from sqlalchemy import select, delete, func
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

    async def get_count(self) -> int:
        """
        Returns the total number of recent projects.

        Invoked By: None.

        Returns:
            int: The project count.
        """
        async with self._db_core.get_async_session() as session:
            statement = select(func.count()).select_from(RecentProjectEntity)
            result = await session.execute(statement)
            return result.scalar_one()

    async def get_oldest_project(self) -> Optional[RecentProject]:
        """
        Retrieves the project with the oldest last_opened_at timestamp.

        Invoked By: None.

        Returns:
            Optional[RecentProject]: The oldest project, or None if no projects exist.
        """
        async with self._db_core.get_async_session() as session:
            statement = select(RecentProjectEntity).order_by(RecentProjectEntity.last_opened_at.asc()).limit(1)
            result = await session.execute(statement)
            entity = result.scalars().first()
            if not entity:
                return None
            return RecentProject(
                id=entity.id,
                name=entity.name,
                path=entity.path,
                last_opened_at=entity.last_opened_at
            )

    async def delete_oldest(self, count: int) -> None:
        """
        Deletes the N oldest projects from the database.

        Invoked By: AddRecentProjectUseCase._enforce_project_limit.

        Args:
            count: The number of oldest projects to delete.
        """
        async with self._db_core.get_async_session() as session:
            subquery = (
                select(RecentProjectEntity.id)
                .order_by(RecentProjectEntity.last_opened_at.asc())
                .limit(count)
                .scalar_subquery()
            )
            statement = delete(RecentProjectEntity).where(RecentProjectEntity.id.in_(subquery))
            await session.execute(statement)
            await session.commit()
