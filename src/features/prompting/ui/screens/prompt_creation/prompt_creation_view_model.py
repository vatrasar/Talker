import os
import asyncio
from features.prompting.domain.models.file_system_item import FileSystemItem
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from features.prompting.ui.screens.prompt_creation.prompt_creation_state import PromptCreationState

class PromptCreationViewModel:
    """
    ViewModel for the PromptCreation screen.

    Purpose: Handles business logic and state management for prompt creation.
    Used In: PromptCreationView.
    """

    def __init__(self):
        self.state = PromptCreationState()

    async def set_project_info(self, name: str, path: str) -> None:
        """
        Updates the state with the current project information and loads its structure.

        Invoked By: PromptCreationView.
        """
        self.state.project_name = name
        self.state.project_path = path
        await self.load_project_structure()

    async def load_project_structure(self) -> None:
        """
        Loads the file system structure of the current project path into the state.

        Invoked By: set_project_info.
        """
        if self._is_invalid_path(self.state.project_path):
            return

        self.state.file_system_tree = await asyncio.to_thread(
            self._scan_directory, 
            self.state.project_path
        )
        self._recalculate_sidebar_width()

    def _is_invalid_path(self, path: str | None) -> bool:
        return not path or not os.path.exists(path)

    def _scan_directory(self, path: str) -> list[FileSystemItem]:
        items = []

        try:
            items = self._get_directory_items(path)
        except PermissionError as e:
            self._handle_scan_error(path, e)
        
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

    async def toggle_folder(self, path: str) -> None:
        """
        Toggles the expansion state of a folder and recalculates sidebar width.
        
        Invoked By: FileBrowserItem.
        """
        new_expanded = set(self.state.expanded_folders)
        if path in new_expanded:
            new_expanded.remove(path)
        else:
            new_expanded.add(path)
            
        self.state.expanded_folders = new_expanded
        self._recalculate_sidebar_width()

    def _recalculate_sidebar_width(self) -> None:
        max_width = 250.0
        
        def process_items(items, level):
            nonlocal max_width
            for item in items:
                # Calculation: level * indent + name_len * char_width + static_ui_parts
                item_width = (level * 20) + (len(item.name) * 8.5) + 85
                max_width = max(max_width, item_width)
                
                if item.type == FileSystemItemType.FOLDER and item.path in self.state.expanded_folders:
                    process_items(item.children, level + 1)
        
        process_items(self.state.file_system_tree, 0)
        self.state.sidebar_width = min(max_width, 600.0)

    def _handle_scan_error(self, path: str, error: Exception) -> None:

        print(f"Warning: Could not scan directory {path}: {error}")
