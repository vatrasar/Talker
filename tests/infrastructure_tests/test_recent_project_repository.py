import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.data.entities.entity_base import BaseEntity
from infrastructure.database.db_core import DBCore
from infrastructure.repositories.recent_project_repository import RecentProjectRepository
from unittest.mock import patch

@pytest_asyncio.fixture
async def mock_db_core():
    # Use in-memory database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)
    
    session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    class MockDBCore(DBCore):
        def __init__(self):
            self.engine = engine
            self.session_factory = session_factory
            
    db_core = MockDBCore()
    yield db_core
    await engine.dispose()

@pytest.mark.asyncio
async def test_add_project_new_path_saves_to_db(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    name = "Test Project"
    path = "/path/to/test"
    
    project = await repo.add_project(name, path)
    
    assert project.name == name
    assert project.path == path
    
    projects = await repo.get_all()
    assert len(projects) == 1
    assert projects[0].name == name
    assert projects[0].path == path

@pytest.mark.asyncio
async def test_add_project_existing_path_updates_name(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    path = "/path/to/test"
    
    await repo.add_project("Old Name", path)
    updated_project = await repo.add_project("New Name", path)
    
    assert updated_project.name == "New Name"
    
    projects = await repo.get_all()
    assert len(projects) == 1
    assert projects[0].name == "New Name"

@pytest.mark.asyncio
async def test_get_all_returns_projects_ordered_by_last_opened_desc(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    
    await repo.add_project("First", "/path/1")
    # Wait a bit or manually adjust if needed, but normally DB default will handle it
    # For testing ordering, we might need to be sure about timestamps
    await repo.add_project("Second", "/path/2")
    
    projects = await repo.get_all()
    assert len(projects) == 2
    # Second project should be first in the list because it was added later
    assert projects[0].name == "Second"
    assert projects[1].name == "First"

@pytest.mark.asyncio
async def test_get_count_returns_correct_number_of_projects(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    
    assert await repo.get_count() == 0
    
    await repo.add_project("P1", "/path/1")
    await repo.add_project("P2", "/path/2")
    
    assert await repo.get_count() == 2

@pytest.mark.asyncio
async def test_get_oldest_project_returns_project_with_earliest_timestamp(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    import asyncio
    
    await repo.add_project("Oldest", "/path/old")
    await asyncio.sleep(0.1)
    await repo.add_project("Newest", "/path/new")
    
    oldest = await repo.get_oldest_project()
    assert oldest.name == "Oldest"
    assert oldest.path == "/path/old"

@pytest.mark.asyncio
async def test_delete_project_removes_project_from_db(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    
    project = await repo.add_project("To Delete", "/path/delete")
    assert await repo.get_count() == 1
    
    await repo.delete_project(project.id)
    assert await repo.get_count() == 0


@pytest.mark.asyncio
async def test_delete_oldest_removes_correct_number_of_oldest_projects(mock_db_core):
    repo = RecentProjectRepository(mock_db_core)
    import asyncio
    
    # Add 5 projects with different timestamps
    for i in range(5):
        await repo.add_project(f"Project {i}", f"/path/{i}")
        await asyncio.sleep(0.01) # Ensure different timestamps
        
    assert await repo.get_count() == 5
    
    # Delete 3 oldest projects (0, 1, 2)
    await repo.delete_oldest(3)
    
    assert await repo.get_count() == 2
    
    projects = await repo.get_all()
    # Remaining projects should be 4 and 3 (get_all returns desc)
    assert projects[0].name == "Project 4"
    assert projects[1].name == "Project 3"
