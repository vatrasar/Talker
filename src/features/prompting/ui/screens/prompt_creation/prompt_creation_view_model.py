import os
from features.prompting.domain.models.file_system_item import FileSystemItem
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from features.prompting.ui.screens.prompt_creation.prompt_creation_state import PromptCreationState
from features.prompting.domain.services.project_structure_service import ProjectStructureService
from core.models.result import Result

class PromptCreationViewModel:
    """
    ViewModel for the PromptCreation screen.

    Purpose: Handles business logic and state management for prompt creation.
    Used In: PromptCreationView.
    """

    def __init__(self, project_structure_service: ProjectStructureService):
        self.state = PromptCreationState()
        self._project_structure_service = project_structure_service

    async def set_project_info(self, name: str, path: str) -> None:
        """
        Updates the state with the current project information and loads its structure.

        Invoked By: PromptCreationView.
        """
        if self.state.project_path != path:
            self._project_structure_service.clear_open_folders()
            self.state.expanded_folders = set()

        self.state.project_name = name
        self.state.project_path = path
        await self.load_project_structure()

    async def load_project_structure(self, show_loading: bool = True) -> None:
        """
        Loads the file system structure of the current project path into the state.

        Invoked By: set_project_info.
        """
        if show_loading:
            self.state.is_loading_files = True
        try:
            result = await self._project_structure_service.get_structure(
                self.state.project_path
            )

            if result.is_success:
                self.state.file_system_tree = result.value
                self._recalculate_sidebar_width()
        finally:
            if show_loading:
                self.state.is_loading_files = False

    async def toggle_folder(self, path: str) -> None:
        """
        Toggles the expansion state of a folder and recalculates sidebar width.
        
        Invoked By: FileBrowserItem.
        """
        if path in self.state.expanded_folders:
            self._project_structure_service.close_folder(path)
        else:
            self._project_structure_service.open_folder(path)
            
        self.state.expanded_folders = self._project_structure_service.get_open_folders()
        await self.load_project_structure(show_loading=False)

    def _recalculate_sidebar_width(self) -> None:
        max_width = self._calculate_max_item_width(self.state.file_system_tree, 0)
        final_width = max(280.0, max_width)
        self.state.sidebar_width = min(final_width, 600.0)

    def _calculate_max_item_width(self, items: list[FileSystemItem], level: int) -> float:
        max_width = 0.0

        for item in items:
            static_width = 70.0
            text_width = (len(item.name) * 7.5) + 10.0
            item_width = (level * 21.0) + text_width + static_width
            max_width = max(max_width, item_width)

            if item.type == FileSystemItemType.FOLDER and item.path in self.state.expanded_folders:
                child_max = self._calculate_max_item_width(item.children, level + 1)
                max_width = max(max_width, child_max)

        return max_width
