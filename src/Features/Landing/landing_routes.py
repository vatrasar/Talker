import flet as ft

from Features.Landing.UI.Screens.ProjectPick.project_pick_view import ProjectPickView

PROJECT_PICK_ROUTE = "/"


def get_landing_routes() -> ft.Route:
    """
    Returns the route tree for the Landing feature.

    Used In: NavHost
    """
    return ft.Route(path=PROJECT_PICK_ROUTE, component=ProjectPickView)
