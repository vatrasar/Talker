import flet as ft
from dataclasses import dataclass

@ft.observable
@dataclass
class PromptCreationState:
    """
    State for the PromptCreation screen.

    Used In: PromptCreationViewModel, PromptCreationView.
    """
    project_name: str = ""
    project_path: str = ""
