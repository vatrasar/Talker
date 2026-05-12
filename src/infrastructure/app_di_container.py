from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel
from infrastructure.database.db_core import DBCore


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

    @property
    def db_core(self) -> DBCore:
        return self._db_core

    def build_project_pick_view_model(self) -> ProjectPickViewModel:
        """
        Builds and returns a new instance of ProjectPickViewModel.

        Returns:
            ProjectPickViewModel: The instantiated ViewModel.
        """
        return ProjectPickViewModel()
