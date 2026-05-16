import os
import asyncio
from features.prompting.domain.models.file_system_item import FileSystemItem
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from core.models.result import Result

class LoadProjectStructureUseCase:
    """
    UseCase for loading the file system structure of a project.
    
    This class handles the recursive scanning of directories to build a tree representation 
    of the project's files and folders.
    """

    async def execute(self, path: str) -> Result[list[FileSystemItem], str]:
        if not path or not os.path.exists(path) or not os.path.isdir(path):
            return Result.fail("Invalid project path")

        items = await asyncio.to_thread(self._scan_directory, path)
        return Result.ok(items)

    def _scan_directory(self, path: str) -> list[FileSystemItem]:
        items = []

        try:
            items = self._get_directory_items(path)
        except PermissionError as e:
            print(f"Warning: Could not scan directory {path}: {e}")
        
        items.sort(key=lambda x: (x.type != FileSystemItemType.FOLDER, x.name.lower()))
        return items

    def _get_directory_items(self, path: str) -> list[FileSystemItem]:
        items = []
        
        for entry in os.scandir(path):
            self._process_directory_entry(entry, items)
            
        return items

    def _process_directory_entry(self, entry: os.DirEntry, items: list[FileSystemItem]) -> None:
        if entry.name.startswith("."):
            return
            
        if entry.is_dir():
            items.append(self._create_folder_item(entry))
            return
            
        items.append(self._create_file_item(entry))

    def _create_folder_item(self, entry: os.DirEntry) -> FileSystemItem:
        return FileSystemItem(
            name=entry.name,
            path=entry.path,
            type=FileSystemItemType.FOLDER,
            children=self._scan_directory(entry.path)
        )

    def _create_file_item(self, entry: os.DirEntry) -> FileSystemItem:
        return FileSystemItem(
            name=entry.name,
            path=entry.path,
            type=FileSystemItemType.FILE
        )

