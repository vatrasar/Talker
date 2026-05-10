import flet as ft
from typing import Callable

from Features.Landing.UI.Screens.ProjectPick.ScreenComponents.recent_project_card import RecentProjectCard


@ft.component
def ProjectPickView():
    """
    The initial landing screen of the application.

    Purpose: Provides the user with options to open existing projects or create a new one.
    Available Functionalities: View recent projects list, navigate to new project creation.
    Key UI Elements: Application logo, welcome header, "Open New Project" button, list of recent projects.
    Navigate From: App Launch
    Navigate To: Feature-specific screens (e.g., Workspace) depending on the selected project.
    """
    page: ft.Page = ft.context.page
    is_xs, set_is_xs = ft.use_state(page.width < 576)

    def handle_resize(e: ft.ControlEvent) -> None:
        set_is_xs(page.width < 576)

    def register_resize():
        page.on_resize = handle_resize
        return lambda: setattr(page, "on_resize", None)

    ft.use_effect(register_resize, [])

    def handle_new_project(e: ft.ControlEvent) -> None:
        pass

    # Main structure assembly
    main_column = ft.Column(
        col={"xs": 12, "sm": 10, "md": 10, "lg": 8, "xl": 8},
        offset={"sm": 1, "md": 1, "lg": 2, "xl": 2},
        controls=[
            LogoSection(),
            WelcomeHeader(is_xs=is_xs, on_new_project=handle_new_project),
            ft.Divider(height=40, color=ft.Colors.OUTLINE_VARIANT),
            RecentProjectsList(is_xs=is_xs),
        ],
        spacing=10,
    )

    return ft.Container(
        content=ft.ListView(
            controls=[
                ft.ResponsiveRow(
                    controls=[main_column],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            spacing=10,
            padding=ft.Padding.symmetric(horizontal=20),
        ),
        bgcolor=ft.Colors.SURFACE,
        padding=ft.Padding.symmetric(vertical=60),
        expand=True,
    )


@ft.component
def LogoSection():
    """Displays the main application logo and name."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.PRIMARY, size=48),
                ft.Text(
                    "Talker",
                    size=40,
                    weight=ft.FontWeight.W_900,
                    color=ft.Colors.PRIMARY,
                    style=ft.TextStyle(letter_spacing=-1),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
        ),
        margin=ft.Margin.only(bottom=80),
        alignment=ft.Alignment.CENTER,
    )


@ft.component
def WelcomeHeader(is_xs: bool, on_new_project: Callable[[ft.ControlEvent], None]):
    """Displays the welcome message and the 'Open New Project' action."""
    welcome_text = ft.Column(
        controls=[
            ft.Text(
                "Welcome back.",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.ON_SURFACE,
                text_align=ft.TextAlign.CENTER if is_xs else ft.TextAlign.LEFT,
            ),
            ft.Text(
                "Here are your recent workspaces.",
                size=14,
                color=ft.Colors.ON_SURFACE_VARIANT,
                text_align=ft.TextAlign.CENTER if is_xs else ft.TextAlign.LEFT,
            ),
        ],
        col={"xs": 12, "sm": 8, "md": 8},
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER if is_xs else ft.CrossAxisAlignment.START,
    )

    new_project_btn = ft.Container(
        content=ft.OutlinedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CREATE_NEW_FOLDER_OUTLINED, size=18, color=ft.Colors.PRIMARY),
                    ft.Text("Open New Project", size=14, color=ft.Colors.PRIMARY, weight=ft.FontWeight.W_500),
                ],
                spacing=8,
                tight=True,
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=4),
                side=ft.BorderSide(1, ft.Colors.OUTLINE),
                padding=ft.Padding.all(16),
                bgcolor=ft.Colors.SURFACE_CONTAINER,
            ),
            on_click=on_new_project,
        ),
        col={"xs": 12, "sm": 4, "md": 4},
        alignment=ft.Alignment.CENTER if is_xs else ft.Alignment.CENTER_RIGHT,
    )

    return ft.ResponsiveRow(
        controls=[welcome_text, new_project_btn],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def RecentProjectsList(is_xs: bool):
    """Displays a column of recent project cards."""
    projects = [
        ("AI Marketing Research", "/Users/admin/Documents/Talker/AI-Marketing-Research", "Updated 2h ago"),
        ("Global Expansion Strategy", "C:\\Projects\\Global-Strategy", "Updated 1d ago"),
        ("Q3 Financials", "/Volumes/Data/Finance/Q3-2024", "Updated 3d ago"),
        ("Product Launch Rev 2", "D:\\Work\\Talker\\Launch-Rev2", "Updated 1w ago"),
        ("Social Media Campaign", "/Users/admin/Projects/Social-Media", "Updated 2w ago"),
        ("Brand Identity Refresh", "C:\\Designs\\Brand-Refresh", "Updated 3w ago"),
        ("Market Analysis 2024", "/Volumes/Data/Reports/Market-Analysis", "Updated 1m ago"),
        ("Investor Pitch Deck", "/Users/admin/Documents/Pitch-Deck", "Updated 2m ago"),
    ]

    return ft.Column(
        controls=[
            RecentProjectCard(
                project_name=name,
                project_path=path,
                updated_ago=ago,
                show_details=not is_xs,
            )
            for name, path, ago in projects
        ],
        spacing=16,
    )
