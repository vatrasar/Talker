import flet as ft
from Infrastructure.nav_host import NavHost
from Shared.GlobalStyles.app_theme import get_app_theme

def main(page: ft.Page) -> None:
    """
    Application entry point.
    
    Initializes the page configuration, instantiates the central NavHost,
    and triggers the initial navigation.

    Args:
        page (ft.Page): The main application page instance provided by Flet.
    """
    page.title = "Talker"
    page.theme = get_app_theme()
    page.theme_mode = ft.ThemeMode.DARK
    
    nav_host = NavHost(page)
    nav_host.start()


ft.run(main)
