from core.models.recent_project import RecentProject
from core.repository_contracts.i_recent_project_repository import IRecentProjectRepository


class AddRecentProjectUseCase:
    """
    Use case responsible for adding or updating a recent project in the database.

    Purpose: Encapsulates the logic for saving a project to the recent projects list.
    Used In: ProjectPickViewModel.
    """

    def __init__(self, recent_project_repository: IRecentProjectRepository) -> None:
        """
        Initializes the use case with a recent project repository.

        Args:
            recent_project_repository: The repository for recent project data.
        """
        self._recent_project_repository = recent_project_repository

    async def execute(self, name: str, path: str) -> RecentProject:
        """
        Adds a new project or updates an existing one's last opened timestamp.

        Invoked By: ProjectPickViewModel.handle_new_project.

        Args:
            name: The display name of the project.
            path: The filesystem path to the project.

        Returns:
            RecentProject: The added or updated project domain model.
        """
        return await self._recent_project_repository.add_project(name, path)
