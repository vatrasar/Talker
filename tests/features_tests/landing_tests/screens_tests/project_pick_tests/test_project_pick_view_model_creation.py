import pytest
from infrastructure.app_di_container import AppDIContainer
from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel


@pytest.mark.asyncio
async def test_build_project_pick_view_model_always_returns_view_model_instance():
    """
    Verifies that the AppDIContainer correctly builds the ProjectPickViewModel.
    """
    # Arrange
    container = AppDIContainer()
    await container.initialize()

    # Act
    vm = container.build_project_pick_view_model()
    await vm.load_recent_projects()

    # Assert
    assert isinstance(vm, ProjectPickViewModel)
    assert vm.state is not None
    # We check if it's a list, even if empty (since DB might be empty in test)
    assert isinstance(vm.state.projects, list)
