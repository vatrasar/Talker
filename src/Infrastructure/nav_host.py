import asyncio

import flet as ft
from typing import Dict, Callable, List

from Core.Base.base_navigation import BaseFeatureNavigation
from Features.Landing.landing_navigation import LandingNavigation

class NavHost:
    """
    Central navigation engine for managing Flet routing.
    
    The NavHost acts as the core dispatcher for the application, initializing feature
    navigations, collecting their routes, and handling Flet's route change and view pop events.
    """

    def __init__(self, page: ft.Page) -> None:
        """
        Initializes the NavHost with the main Flet page.

        Args:
            page (ft.Page): The main application page instance.
        """
        self._page: ft.Page = page
        self._feature_navigations: List[BaseFeatureNavigation] = [
            LandingNavigation()
        ]
        self._routes: Dict[str, Callable[[], ft.View]] = {}
        
        self._register_routes()
        self._setup_page_events()

    def _register_routes(self) -> None:
        """
        Iterates over all feature navigations and populates the central routes dictionary.
        """
        for feature_nav in self._feature_navigations:
            self._routes.update(feature_nav.get_routes())

    def _setup_page_events(self) -> None:
        """
        Configures Flet page routing event handlers.
        """
        self._page.on_route_change = self._on_route_change
        self._page.on_view_pop = self._on_view_pop

    def _on_route_change(self) -> None:
        """
        Handles the event triggered when the route changes.

        Finds the corresponding view builder function for the requested route
        and appends the new view to the page's views list. Handles fallback for unknown routes.
        """
        self._page.views.clear()

        if self._page.route not in self._routes:
            fallback_view = ft.View(
                self._page.route,
                [
                    ft.AppBar(title=ft.Text("Route Not Found"), bgcolor=ft.Colors.ERROR_CONTAINER),
                    ft.Text(f"Could not find route: {self._page.route}", size=20)
                ]
            )
            self._page.views.append(fallback_view)
        else:
            view_builder = self._routes[self._page.route]
            self._page.views.append(view_builder())

        self._page.update()

    async def _on_view_pop(self, e: ft.ViewPopEvent) -> None:
        """
        Handles the event when a view is popped (e.g., user presses the back button).

        Removes the topmost view from the stack and navigates to the underlying view.

        Args:
            e (ft.ViewPopEvent): The view pop event data.
        """
        if e.view is not None:
            self._page.views.remove(e.view)
            top_view = self._page.views[-1]
            await self._page.push_route(top_view.route)

    def start(self) -> None:
        """
        Performs the initial navigation by directly invoking the route change handler.
        """
        self._on_route_change()

    def navigate_to(self, route: str) -> None:
        """
        Navigates to the specified route.

        Args:
            route (str): The route path to navigate to.
        """
        asyncio.create_task(self._page.push_route(route))
