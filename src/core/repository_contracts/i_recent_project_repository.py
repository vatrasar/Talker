from abc import ABC, abstractmethod
from typing import List, Optional
from core.models.recent_project import RecentProject


class IRecentProjectRepository(ABC):
    """
    Interface for RecentProject repository.

    Purpose: Defines the contract for managing recent project data.
    Used In: RecentProjectRepository, AppDIContainer.
    """

    @abstractmethod
    async def get_all(self) -> List[RecentProject]:
        """
        Retrieves all recent projects.

        Returns:
            List[RecentProject]: List of all recent projects.
        """
        pass

    @abstractmethod
    async def add_project(self, name: str, path: str) -> RecentProject:
        """
        Adds or updates a recent project.

        Args:
            name: The project name.
            path: The project filesystem path.

        Returns:
            RecentProject: The created or updated project.
        """
        pass

    @abstractmethod
    async def delete_project(self, project_id: int) -> None:
        """
        Deletes a recent project by its ID.

        Args:
            project_id: The unique identifier of the project.
        """
        pass

    @abstractmethod
    async def get_count(self) -> int:
        """
        Returns the total number of recent projects.

        Returns:
            int: The project count.
        """
        pass

    @abstractmethod
    async def get_oldest_project(self) -> Optional[RecentProject]:
        """
        Retrieves the project with the oldest last_opened_at timestamp.

        Returns:
            Optional[RecentProject]: The oldest project, or None if no projects exist.
        """
        pass

    @abstractmethod
    async def delete_oldest(self, count: int) -> None:
        """
        Deletes the N oldest projects from the repository.

        Args:
            count: The number of oldest projects to delete.
        """
        pass
