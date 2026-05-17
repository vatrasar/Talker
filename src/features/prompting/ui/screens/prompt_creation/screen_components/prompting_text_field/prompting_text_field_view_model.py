from features.prompting.domain.services.prompting_creation_service import PromptingCreationService
from features.prompting.domain.use_cases.merge_prompt_text_use_case import MergePromptTextUseCase
from features.prompting.ui.screens.prompt_creation.screen_components.prompting_text_field.prompting_text_field_state import PromptingTextFieldState

class PromptingTextFieldViewModel:
    """
    ViewModel class for the PromptingTextField smart component.

    Purpose: Coordinates state changes between the Flet UI and PromptingCreationService.
    """

    def __init__(
        self,
        prompting_creation_service: PromptingCreationService,
        merge_prompt_text_use_case: MergePromptTextUseCase,
    ) -> None:
        self.prompting_creation_service = prompting_creation_service
        self._merge_prompt_text_use_case = merge_prompt_text_use_case
        self.state = PromptingTextFieldState()
        self._merged_indices: list[int] = []

    def update_props(self, label: str) -> None:
        """
        Updates the component's state properties and loads starting prompt items.
        """
        self.state.label = label
        self.load_items()

    def load_items(self) -> None:
        """
        Loads the current prompt items from the service and updates reactive state.
        """
        all_items = self.prompting_creation_service.get_items()
        if self._merged_indices:
            self.state.items = [item for i, item in enumerate(all_items) if i not in self._merged_indices]
        else:
            self.state.items = all_items

    def update_text(self, value: str) -> None:
        """
        Updates the temporary typing value in both the reactive state and service.
        """
        self.state.value = value
        self.prompting_creation_service.update(value)

    def add_text_to_prompt(self) -> None:
        """
        Submits the currently typed text buffer to the service to split it into words,
        clears the typing value, and reloads prompt items.
        """
        val = self.state.value
        if val:
            self.prompting_creation_service.addNewText(val)
            self.state.value = ""
            self.load_items()

    async def handle_focus(self) -> None:
        """
        Handles text field focus by merging trailing words into the text field's editing value.
        """
        all_items = self.prompting_creation_service.get_items()
        merged_text, merged_indices = await self._merge_prompt_text_use_case.execute(all_items)
        self._merged_indices = merged_indices
        self.state.value = merged_text
        self.prompting_creation_service.update(merged_text)
        self.load_items()

    async def finish_editing(self) -> None:
        """
        Sends the final edited text and the list of merged indices to the service to finalize editing.
        """
        val = self.state.value
        self.prompting_creation_service.replace_merged_text(val, self._merged_indices)
        self.state.value = ""
        self._merged_indices = []
        self.load_items()

