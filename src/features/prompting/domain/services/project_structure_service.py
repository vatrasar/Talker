import os
import asyncio
from features.prompting.domain.models.file_system_item import FileSystemItem
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from core.models.result import Result

class ProjectStructureService:
    """
    Service for managing and loading the project file structure efficiently.
    
    This service maintains a list of 'open' folders and only scans those folders 
    to improve performance when dealing with large projects.
    """

    def __init__(self) -> None:
        self._open_folders: set[str] = set()

    def open_folder(self, path: str) -> None:
        """
        Adds a folder to the set of open folders.
        
        Invoked By: PromptCreationViewModel.
        """
        self._open_folders.add(path)

    def close_folder(self, path: str) -> None:
        """
        Removes a folder from the set of open folders.
        
        Invoked By: PromptCreationViewModel.
        """
        if path in self._open_folders:
            self._open_folders.remove(path)

    def clear_open_folders(self) -> None:
        """
        Clears all open folders.
        
        Invoked By: PromptCreationViewModel.
        """
        self._open_folders.clear()

    def get_open_folders(self) -> set[str]:
        """
        Returns the set of currently open folders.
        
        Invoked By: PromptCreationViewModel.
        """
        return set(self._open_folders)

    async def get_structure(self, root_path: str) -> Result[list[FileSystemItem], str]:
        """
        Loads the file system structure starting from the root path, scanning only open folders.
        
        Invoked By: PromptCreationViewModel.
        """
        if not root_path or not os.path.exists(root_path) or not os.path.isdir(root_path):
            return Result.fail("Invalid project path")

        items = await asyncio.to_thread(self._scan_directory, root_path)
        return Result.ok(items)

    def _scan_directory(self, path: str) -> list[FileSystemItem]:
        items = []

        try:
            for entry in os.scandir(path):
                if entry.name.startswith("."):
                    continue
                
                item = self._create_item(entry)
                
                # Recursively scan only if it's a folder and it's open
                if item.type == FileSystemItemType.FOLDER and entry.path in self._open_folders:
                    item.children = self._scan_directory(entry.path)
                
                items.append(item)
        except PermissionError as e:
            print(f"Warning: Could not scan directory {path}: {e}")
        
        items.sort(key=lambda x: (x.type != FileSystemItemType.FOLDER, x.name.lower()))
        return items

    def _create_item(self, entry: os.DirEntry) -> FileSystemItem:
        item_type = FileSystemItemType.FOLDER if entry.is_dir() else FileSystemItemType.FILE
        return FileSystemItem(
            name=entry.name,
            path=entry.path,
            type=item_type,
            children=[]
        )
