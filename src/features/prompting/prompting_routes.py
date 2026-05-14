import flet as ft

PROMPTS_ROUTE = "/prompts"


def get_prompting_routes() -> ft.Route:
    """
    Returns the route tree for the Prompting feature.

    Used In: NavHost
    """
    # Placeholder component as we are only creating the skeleton
    @ft.component
    def PromptingPlaceholder():
        return ft.Text("Prompting Feature Skeleton")

    return ft.Route(path=PROMPTS_ROUTE, component=PromptingPlaceholder)
