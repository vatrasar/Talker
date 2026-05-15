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
        if not self.state.project_path or not os.path.exists(self.state.project_path):
            return

        def _scan_directory(path: str) -> list[FileSystemItem]:
            items = []
            try:
                for entry in os.scandir(path):
                    if entry.name.startswith("."):
                        continue
                        
                    if entry.is_dir():
                        items.append(FileSystemItem(
                            name=entry.name,
                            type=FileSystemItemType.FOLDER,
                            children=_scan_directory(entry.path)
                        ))
                    else:
                        items.append(FileSystemItem(
                            name=entry.name,
                            type=FileSystemItemType.FILE
                        ))
            except PermissionError:
                pass
            
            items.sort(key=lambda x: (x.type != FileSystemItemType.FOLDER, x.name.lower()))
            return items

        self.state.file_system_tree = await asyncio.to_thread(_scan_directory, self.state.project_path)
