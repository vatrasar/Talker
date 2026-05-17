from features.prompting.domain.models.item_in_sorted_list import ItemInSortedList

class MergePromptTextUseCase:
    """
    Use case responsible for merging text words immediately to the left of the active text field.

    Purpose: Merges consecutive string items from the end of the item list into a single string.
    Used In: PromptingTextFieldViewModel.
    """

    async def execute(self, items: list[ItemInSortedList]) -> tuple[str, list[int]]:
        merged_words = []
        merged_indices = []
        for i in range(len(items) - 1, -1, -1):
            item = items[i]
            if isinstance(item.value, str):
                merged_words.insert(0, item.value)
                merged_indices.insert(0, i)
            else:
                break

        merged_text = " ".join(merged_words)
        return merged_text, merged_indices
