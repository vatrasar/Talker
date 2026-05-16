from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel
from core.repository_contracts.i_recent_project_repository import IRecentProjectRepository
from infrastructure.database.db_core import DBCore
from infrastructure.repositories.recent_project_repository import RecentProjectRepository
from features.landing.domain.use_cases.add_recent_project_use_case import AddRecentProjectUseCase
from features.prompting.domain.use_cases.load_project_structure_use_case import LoadProjectStructureUseCase


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
        self._recent_project_repository = RecentProjectRepository(self._db_core)
        self._add_recent_project_use_case = AddRecentProjectUseCase(self._recent_project_repository)
        self._load_project_structure_use_case = LoadProjectStructureUseCase()

    async def initialize(self) -> None:
        """
        Performs asynchronous initialization of the container's dependencies.
        """
        await self._db_core.init_db_schema()

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
        return ProjectPickViewModel(
            add_recent_project_use_case=self._add_recent_project_use_case,
            recent_project_repository=self._recent_project_repository
        )

    def build_prompt_creation_view_model(self) -> PromptCreationViewModel:
        """
        Builds and returns a new instance of PromptCreationViewModel.

        Returns:
            PromptCreationViewModel: The instantiated ViewModel.
        """
        return PromptCreationViewModel(
            load_project_structure_use_case=self._load_project_structure_use_case
        )
