import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from features.landing.domain.use_cases.add_recent_project_use_case import AddRecentProjectUseCase
from core.models.recent_project import RecentProject


@pytest.mark.asyncio
async def test_execute_calls_repository_with_correct_data_and_returns_result():
    """
    Verifies that the use case calls the repository with correct data and returns the result.
    """
    # Arrange
    mock_repo = MagicMock()
    mock_repo.add_project = AsyncMock()
    mock_repo.get_count = AsyncMock(return_value=1)
    
    expected_project = RecentProject(id=1, name="Test", path="/path", last_opened_at=None)
    mock_repo.add_project.return_value = expected_project
    
    use_case = AddRecentProjectUseCase(mock_repo)
    
    # Act
    result = await use_case.execute("Test", "/path")
    
    # Assert
    mock_repo.add_project.assert_called_once_with("Test", "/path")
    assert result == expected_project


@pytest.mark.asyncio
async def test_execute_removes_oldest_project_when_limit_exceeded():
    """
    Verifies that the oldest projects are deleted when the project count exceeds the limit.
    """
    # Arrange
    mock_repo = MagicMock()
    mock_repo.add_project = AsyncMock()
    # First call returns 31, second returns 30 (final verification)
    mock_repo.get_count = AsyncMock(side_effect=[31, 30])
    mock_repo.delete_oldest = AsyncMock()
    
    use_case = AddRecentProjectUseCase(mock_repo)
    
    # Act
    with patch("features.landing.domain.use_cases.add_recent_project_use_case.MAX_RECENT_PROJECTS", 30):
        await use_case.execute("New Project", "/new")
    
    # Assert
    assert mock_repo.get_count.call_count == 2
    mock_repo.delete_oldest.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_execute_does_not_remove_project_when_under_limit():
    """
    Verifies that no project is deleted when the project count is within the limit.
    """
    # Arrange
    mock_repo = MagicMock()
    mock_repo.add_project = AsyncMock()
    mock_repo.get_count = AsyncMock(return_value=25)
    mock_repo.delete_oldest = AsyncMock()
    
    use_case = AddRecentProjectUseCase(mock_repo)
    
    # Act
    with patch("features.landing.domain.use_cases.add_recent_project_use_case.MAX_RECENT_PROJECTS", 30):
        await use_case.execute("New Project", "/new")
    
    # Assert
    mock_repo.get_count.assert_called_once()
    mock_repo.delete_oldest.assert_not_called()


@pytest.mark.asyncio
async def test_execute_removes_multiple_projects_when_limit_exceeded_by_more_than_one():
    """
    Verifies that the use case deletes multiple oldest projects if the count is much higher than the limit.
    """
    # Arrange
    mock_repo = MagicMock()
    mock_repo.add_project = AsyncMock()
    # First call returns 35, second returns 30
    mock_repo.get_count = AsyncMock(side_effect=[35, 30])
    mock_repo.delete_oldest = AsyncMock()
    
    use_case = AddRecentProjectUseCase(mock_repo)
    
    # Act
    with patch("features.landing.domain.use_cases.add_recent_project_use_case.MAX_RECENT_PROJECTS", 30):
        await use_case.execute("New Project", "/new")
    
    # Assert
    assert mock_repo.get_count.call_count == 2
    mock_repo.delete_oldest.assert_called_once_with(5)
