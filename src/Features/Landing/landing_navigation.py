import flet as ft
from typing import Dict, Callable

from Core.Base.base_navigation import BaseFeatureNavigation
from Features.Landing.UI.Screens.ProjectPick.project_pick_view import ProjectPickView

class LandingNavigation(BaseFeatureNavigation):
    """
    Registers routing paths for the Landing feature.
    
    Purpose: Provides the view builder functions for the Landing screens.
    Usage: Instantiated and registered within the central NavHost.
    Used In: NavHost
    """

    def __init__(self) -> None:
        super().__init__()

    def get_routes(self) -> Dict[str, Callable[[], ft.View]]:
        return {
            "/": lambda: ProjectPickView(route="/")
        }
