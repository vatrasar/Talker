from core.config import MAX_RECENT_PROJECTS
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
        If the total count exceeds MAX_RECENT_PROJECTS, the oldest project is removed.

        Invoked By: ProjectPickViewModel.handle_new_project.

        Args:
            name: The display name of the project.
            path: The filesystem path to the project.

        Returns:
            RecentProject: The added or updated project domain model.
        """
        project = await self._recent_project_repository.add_project(name, path)
        await self._enforce_project_limit()

        return project

    async def _enforce_project_limit(self) -> None:
        """
        Ensures the number of recent projects does not exceed MAX_RECENT_PROJECTS.
        Calculates excess projects and deletes them in bulk.
        """
        count = await self._recent_project_repository.get_count()

        if count > MAX_RECENT_PROJECTS:
            excess = count - MAX_RECENT_PROJECTS
            await self._recent_project_repository.delete_oldest(excess)

            # Final verification as requested by the user
            new_count = await self._recent_project_repository.get_count()

