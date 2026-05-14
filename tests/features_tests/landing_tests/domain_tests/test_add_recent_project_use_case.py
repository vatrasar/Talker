import pytest
from unittest.mock import AsyncMock, MagicMock
from features.landing.domain.use_cases.add_recent_project_use_case import AddRecentProjectUseCase
from core.models.recent_project import RecentProject

@pytest.mark.asyncio
async def test_execute_calls_repository_with_correct_data_and_returns_result():
    # Arrange
    mock_repo = MagicMock()
    mock_repo.add_project = AsyncMock()
    
    expected_project = RecentProject(id=1, name="Test", path="/path", last_opened_at=None)
    mock_repo.add_project.return_value = expected_project
    
    use_case = AddRecentProjectUseCase(mock_repo)
    
    # Act
    result = await use_case.execute("Test", "/path")
    
    # Assert
    mock_repo.add_project.assert_called_once_with("Test", "/path")
    assert result == expected_project
