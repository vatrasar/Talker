import flet as ft
from infrastructure.nav_host import NavHost
from shared.global_styles.app_theme import get_app_theme


def main(page: ft.Page) -> None:
    """
    Application entry point.

    Initializes page configuration and renders the declarative NavHost component.

    Args:
        page (ft.Page): The main application page instance provided by Flet.
    """
    page.title = "Talker"
    page.theme = get_app_theme()
    page.theme_mode = ft.ThemeMode.DARK

    # Initialize Dependency Injection container
    from infrastructure.app_di_container import AppDIContainer
    page.session.store.set("di_container", AppDIContainer())

    page.render(NavHost)


ft.run(main)
