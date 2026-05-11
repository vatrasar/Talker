from infrastructure.app_di_container import AppDIContainer
from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel


def test_build_project_pick_view_model_always_returns_view_model_instance():
    """
    Verifies that the AppDIContainer correctly builds the ProjectPickViewModel.
    """
    # Arrange
    container = AppDIContainer()

    # Act
    vm = container.build_project_pick_view_model()

    # Assert
    assert isinstance(vm, ProjectPickViewModel)
    assert vm.state is not None
    assert len(vm.state.projects) > 0
