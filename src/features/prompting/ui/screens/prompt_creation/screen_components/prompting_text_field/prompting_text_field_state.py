from dataclasses import dataclass, field
import flet as ft
from features.prompting.domain.models.item_in_sorted_list import ItemInSortedList

@ft.observable
@dataclass
class PromptingTextFieldState:
    """
    State class representing the reactive UI state of PromptingTextField.

    Used In: PromptingTextFieldViewModel and PromptingTextFieldView.
    """
    label: str = ""
    value: str = ""
    items: list[ItemInSortedList] = field(default_factory=list)
