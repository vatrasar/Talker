from dataclasses import dataclass
from typing import Union
from features.prompting.domain.models.file_system_item_for_prompt import FileSystemItemForPrompt

@dataclass
class ItemInSortedList:
    """
    Model representing an indexed item inside the prompt creation list.

    Used In: PromptingCreationService, PromptingTextFieldState, PromptingTextFieldViewModel.
    """
    index: int
    value: Union[str, FileSystemItemForPrompt]
