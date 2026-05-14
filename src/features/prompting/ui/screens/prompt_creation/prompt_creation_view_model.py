from features.prompting.ui.screens.prompt_creation.prompt_creation_state import PromptCreationState

class PromptCreationViewModel:
    """
    ViewModel for the PromptCreation screen.

    Purpose: Handles business logic and state management for prompt creation.
    Used In: PromptCreationView.
    """

    def __init__(self):
        self.state = PromptCreationState()

    def set_project_info(self, name: str, path: str) -> None:
        """
        Updates the state with the current project information.

        Invoked By: PromptCreationView.
        """
        self.state.project_name = name
        self.state.project_path = path
