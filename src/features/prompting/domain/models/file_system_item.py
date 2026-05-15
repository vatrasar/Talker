from dataclasses import dataclass, field
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType

@dataclass
class FileSystemItem:
    """
    Model representing a file or folder in the project structure.
    
    Used In: PromptCreationState, PromptCreationViewModel, FileBrowserSidebar.
    """
    name: str
    path: str
    type: FileSystemItemType
    children: list["FileSystemItem"] = field(default_factory=list)
