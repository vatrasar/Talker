import copy
from features.prompting.domain.models.item_in_sorted_list import ItemInSortedList

class PromptingCreationService:
    """
    Service for managing the elements that compose the generated prompt.

    This service tracks the ordered list of text words and filesystem items (files/folders)
    that make up the prompt, ensuring proper formatting and single-word splitting.
    """

    def __init__(self) -> None:
        self._items: list[ItemInSortedList] = []
        self._current_text: str = ""

    @property
    def current_text(self) -> str:
        """
        Returns the current temporary text typed in the prompt editing field.
        """
        return self._current_text

    def update(self, text: str) -> None:
        """
        Updates the current temporary text buffer as the user is typing.
        """
        self._current_text = text

    def addNewText(self, text: str) -> None:
        """
        Splits a string by space into single-word items and adds them to the sorted list.
        """
        if not text or not text.strip():
            self._current_text = ""
            return

        words = text.split()
        for word in words:
            next_index = len(self._items)
            item = ItemInSortedList(index=next_index, value=word)
            self._items.append(item)
        self._current_text = ""

    def get_items(self) -> list[ItemInSortedList]:
        """
        Returns a deep copy of the sorted items making up the prompt.
        """
        return copy.deepcopy(self._items)

    def replace_merged_text(self, text: str, merged_indices: list[int]) -> None:
        """
        Removes the merged words at specified indices and adds the new text split into words.

        Invoked By: PromptingTextFieldViewModel.
        """
        self._items = [item for idx, item in enumerate(self._items) if idx not in merged_indices]

        if text and text.strip():
            words = text.split()
            for word in words:
                next_index = len(self._items)
                item = ItemInSortedList(index=next_index, value=word)
                self._items.append(item)

        for idx, item in enumerate(self._items):
            item.index = idx

        self._current_text = ""

