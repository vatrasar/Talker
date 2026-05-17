from features.prompting.domain.services.prompting_creation_service import PromptingCreationService
from features.prompting.ui.screens.prompt_creation.screen_components.prompting_text_field.prompting_text_field_state import PromptingTextFieldState

class PromptingTextFieldViewModel:
    """
    ViewModel class for the PromptingTextField smart component.

    Purpose: Coordinates state changes between the Flet UI and PromptingCreationService.
    """

    def __init__(self, prompting_creation_service: PromptingCreationService) -> None:
        self.prompting_creation_service = prompting_creation_service
        self.state = PromptingTextFieldState()

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
        self.state.items = self.prompting_creation_service.get_items()

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
