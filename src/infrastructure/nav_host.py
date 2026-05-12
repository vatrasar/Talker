import flet as ft

from features.landing.landing_routes import get_landing_routes


@ft.component
def NavHost():
    """
    Central navigation engine for the application.

    Aggregates all feature routes into a single ft.Router
    and serves as the root component rendered by page.render().
    """
    return ft.Router(
        routes=[
            get_landing_routes(),
        ],
        manage_views=False,
    )
