import os
from features.prompting.domain.models.file_system_item import FileSystemItem
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from features.prompting.ui.screens.prompt_creation.prompt_creation_state import PromptCreationState
from features.prompting.domain.use_cases.load_project_structure_use_case import LoadProjectStructureUseCase
from core.models.result import Result

class PromptCreationViewModel:
    """
    ViewModel for the PromptCreation screen.

    Purpose: Handles business logic and state management for prompt creation.
    Used In: PromptCreationView.
    """

    def __init__(self, load_project_structure_use_case: LoadProjectStructureUseCase):
        self.state = PromptCreationState()
        self._load_project_structure_use_case = load_project_structure_use_case

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
        self.state.is_loading_files = True
        try:
            result = await self._load_project_structure_use_case.execute(
                self.state.project_path
            )

            if result.is_success:
                self.state.file_system_tree = result.value
                self._recalculate_sidebar_width()
        finally:
            self.state.is_loading_files = False


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
                # Dokładne wyliczenie stałych marginesów i ikon dla folderów i plików
                if item.type == FileSystemItemType.FOLDER:
                    # icon(18) + btn(24) + spacing(16) + item_pad(8) + root_pad(30)
                    static_width = 96 
                else:
                    # icon(18) + spacing(8) + item_pad(8) + root_pad(30)
                    static_width = 64
                    
                # level offset (10 margin + 10 padding + 1 border = 21px na poziom)
                # 6.5px to realistyczna średnia dla czcionki 13pt.
                # Dodajemy płaski bufor 15px na wypadek szerszych znaków.
                text_width = (len(item.name) * 6.5) + 15
                item_width = (level * 21) + text_width + static_width
                max_width = max(max_width, item_width)
                
                if item.type == FileSystemItemType.FOLDER and item.path in self.state.expanded_folders:
                    process_items(item.children, level + 1)
        
        process_items(self.state.file_system_tree, 0)
        self.state.sidebar_width = min(max_width, 600.0)
