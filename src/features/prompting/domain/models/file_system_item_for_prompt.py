from dataclasses import dataclass
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType

@dataclass
class FileSystemItemForPrompt:
    """
    Model representing a flat file or folder in the project structure for a prompt.

    Used In: ItemInSortedList, PromptingCreationService, PromptingTextFieldViewModel.
    """
    name: str
    path: str
    type: FileSystemItemType
