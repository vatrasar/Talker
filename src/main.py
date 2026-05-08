import flet as ft
from Infrastructure.nav_host import NavHost

def main(page: ft.Page) -> None:
    """
    Application entry point.
    
    Initializes the page configuration, instantiates the central NavHost,
    and triggers the initial navigation.

    Args:
        page (ft.Page): The main application page instance provided by Flet.
    """
    page.title = "Talker"
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    nav_host = NavHost(page)
    nav_host.navigate_to("/")


ft.run(main)
