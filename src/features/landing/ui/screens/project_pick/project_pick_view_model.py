import os
import flet as ft
from datetime import datetime, UTC
from features.landing.domain.models.project import Project
from features.landing.ui.screens.project_pick.project_pick_state import ProjectPickState
from features.landing.domain.use_cases.add_recent_project_use_case import AddRecentProjectUseCase
from core.repository_contracts.i_recent_project_repository import IRecentProjectRepository


class ProjectPickViewModel:
    """
    ViewModel for the ProjectPick screen.

    Purpose: Handles business logic and state management for project selection.
    Used In: ProjectPickView.
    """

    def __init__(
        self,
        add_recent_project_use_case: AddRecentProjectUseCase,
        recent_project_repository: IRecentProjectRepository
    ):
        self.state = ProjectPickState()
        self._add_recent_project_use_case = add_recent_project_use_case
        self._recent_project_repository = recent_project_repository

    async def handle_folder_selected(self, path: str) -> None:
        """
        Handles the logic after a folder has been selected.

        Invoked By: ProjectPickView.
        """
        name = os.path.basename(path.rstrip(os.sep)) or path
        result = await self._add_recent_project_use_case.execute(name, path)
        if result.is_success:
            await self.load_recent_projects()
        else:
            print(f"Failed to add project: {result.error}")

    async def load_recent_projects(self) -> None:
        """
        Loads the list of recent projects from the database.
        """
        recent_projects = await self._recent_project_repository.get_all()
        self.state.projects = [
            Project(
                name=p.name,
                path=p.path,
                updated_ago=self._format_last_opened(p.last_opened_at)
            ) for p in recent_projects
        ]

    def _format_last_opened(self, last_opened: datetime) -> str:
        """
        Formats the last opened timestamp into a human-readable 'Updated ... ago' string.
        """
        diff = datetime.now(UTC).replace(tzinfo=None) - last_opened
        if diff.days > 0:
            return f"Updated {diff.days}d ago"
        hours = diff.seconds // 3600
        if hours > 0:
            return f"Updated {hours}h ago"
        minutes = (diff.seconds % 3600) // 60
        return f"Updated {minutes}m ago"
