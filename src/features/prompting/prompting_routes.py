import flet as ft
from features.prompting.ui.screens.prompt_creation.prompt_creation_view import PromptCreationView

PROMPTS_ROUTE = "/prompts"
PROMPT_CREATION_ROUTE = "/prompts/create/:project_name/:project_path"


def get_prompting_routes() -> list[ft.Route]:
    """
    Returns the route tree for the Prompting feature.

    Used In: NavHost
    """
    return [
        ft.Route(path=PROMPT_CREATION_ROUTE, component=PromptCreationView),
    ]
