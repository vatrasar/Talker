import pytest
from unittest.mock import AsyncMock, MagicMock
from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel
from core.models.recent_project import RecentProject
from datetime import datetime, UTC

@pytest.mark.asyncio
async def test_handle_folder_selected_calls_use_case_and_reloads_projects():
    # Arrange
    mock_use_case = MagicMock()
    mock_use_case.execute = AsyncMock()
    
    mock_repo = MagicMock()
    mock_repo.get_all = AsyncMock(return_value=[])
    
    vm = ProjectPickViewModel(mock_use_case, mock_repo)
    path = "/some/path"
    
    # Act
    await vm.handle_folder_selected(path)
    
    # Assert
    mock_use_case.execute.assert_called_once_with("path", path)
    mock_repo.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_load_recent_projects_updates_state_with_formatted_date():
    # Arrange
    mock_use_case = MagicMock()
    mock_repo = MagicMock()
    
    recent_at = datetime(2024, 1, 1, 12, 0, 0)
    mock_repo.get_all = AsyncMock(return_value=[
        RecentProject(id=1, name="Project 1", path="/p1", last_opened_at=recent_at)
    ])
    
    vm = ProjectPickViewModel(mock_use_case, mock_repo)
    
    # Act
    await vm.load_recent_projects()
    
    # Assert
    assert len(vm.state.projects) == 1
    assert vm.state.projects[0].name == "Project 1"
    assert vm.state.projects[0].path == "/p1"
    assert "Updated" in vm.state.projects[0].updated_ago
