import flet as ft
from dataclasses import dataclass, field
from features.prompting.domain.models.file_system_item import FileSystemItem

@ft.observable
@dataclass
class PromptCreationState:
    """
    State for the PromptCreation screen.

    Used In: PromptCreationViewModel, PromptCreationView.
    """
    project_name: str = ""
    project_path: str = ""
    file_system_tree: list[FileSystemItem] = field(default_factory=list)
    expanded_folders: set[str] = field(default_factory=set)
    sidebar_width: float = 280.0
