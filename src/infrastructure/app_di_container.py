from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel


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
        # Placeholder for singleton services/repositories
        # self.project_service = ProjectService()
        pass

    def build_project_pick_view_model(self) -> ProjectPickViewModel:
        """
        Builds and returns a new instance of ProjectPickViewModel.

        Returns:
            ProjectPickViewModel: The instantiated ViewModel.
        """
        return ProjectPickViewModel()
