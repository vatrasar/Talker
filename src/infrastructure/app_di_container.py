from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel
from core.repository_contracts.i_recent_project_repository import IRecentProjectRepository
from infrastructure.database.db_core import DBCore
from infrastructure.repositories.recent_project_repository import RecentProjectRepository


class AppDIContainer:
    """
    Simplified Dependency Injection container for the application.

    Purpose: Holds singleton instances of services/repositories and provides
    build methods for ViewModels.
    """

    def __init__(self) -> None:
        """
        Initializes the container and its shared dependencies.
        """
        self._db_core = DBCore()
        self._db_core.init_db_schema()
        self._recent_project_repository = RecentProjectRepository(self._db_core)

    @property
    def db_core(self) -> DBCore:
        return self._db_core

    @property
    def recent_project_repository(self) -> IRecentProjectRepository:
        return self._recent_project_repository

    def build_project_pick_view_model(self) -> ProjectPickViewModel:
        """
        Builds and returns a new instance of ProjectPickViewModel.

        Returns:
            ProjectPickViewModel: The instantiated ViewModel.
        """
        return ProjectPickViewModel()
