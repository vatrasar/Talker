from abc import ABC, abstractmethod
from typing import List
from core.models.recent_project import RecentProject


class IRecentProjectRepository(ABC):
    """
    Interface for RecentProject repository.

    Purpose: Defines the contract for managing recent project data.
    Used In: RecentProjectRepository, AppDIContainer.
    """

    @abstractmethod
    def get_all(self) -> List[RecentProject]:
        """
        Retrieves all recent projects.

        Returns:
            List[RecentProject]: List of all recent projects.
        """
        pass

    @abstractmethod
    def add_project(self, name: str, path: str) -> RecentProject:
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
    def delete_project(self, project_id: int) -> None:
        """
        Deletes a recent project by its ID.

        Args:
            project_id: The unique identifier of the project.
        """
        pass
