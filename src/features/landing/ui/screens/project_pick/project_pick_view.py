import flet as ft
from typing import Callable

from features.landing.ui.screens.project_pick.screen_components.recent_project_card import RecentProjectCard
from features.landing.ui.screens.project_pick.screen_styles.project_pick_styles import ProjectPickStyles as Styles
from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel
from features.landing.domain.models.project import Project


@ft.component
def ProjectPickView() -> ft.Container:
    """
    The initial landing screen of the application.

    Purpose: Provides the user with options to open existing projects or create a new one.
    Available Functionalities: View recent projects list, navigate to new project creation.
    Key UI Elements: Application logo, welcome header with new project button, "Open New Project" button, list of recent projects.
    Bindings: Uses ProjectPickViewModel for state and actions.
    Navigate From: App Launch.
    Navigate To: Feature-specific screens (e.g., Workspace) depending on the selected project.
    Used In: landing_routes.py.
    """
    page: ft.Page = ft.context.page
    vm = ft.use_memo(ProjectPickViewModel, [])
    is_xs, set_is_xs = ft.use_state(page.width < 576)

    def handle_resize(e: ft.ControlEvent) -> None:
        set_is_xs(page.width < 576)

    def register_resize():
        page.on_resize = handle_resize
        return lambda: setattr(page, "on_resize", None)

    ft.use_effect(register_resize, [])

    # Main structure assembly
    main_column = ft.Column(
        col={"xs": 12, "sm": 10, "md": 10, "lg": 8, "xl": 8},
        offset={"sm": 1, "md": 1, "lg": 2, "xl": 2},
        controls=[
            LogoSection(),
            WelcomeHeaderWithNewProject(is_xs=is_xs, on_new_project=vm.handle_new_project),
            ft.Divider(height=40, color=ft.Colors.OUTLINE_VARIANT),
            RecentProjectsList(is_xs=is_xs, projects=vm.state.projects),
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
def LogoSection() -> ft.Container:
    """
    Displays the main application logo and name.

    Purpose: Branding and identification.
    Key UI Elements: Icon, Text.
    Used In: ProjectPickView.
    """
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.PRIMARY, size=48),
                ft.Text(
                    "Talker",
                    style=Styles.LOGO_TEXT_STYLE,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
        ),
        margin=ft.Margin.only(bottom=80),
        alignment=ft.Alignment.CENTER,
    )


@ft.component
def WelcomeHeaderWithNewProject(is_xs: bool, on_new_project: Callable[[ft.ControlEvent], None]) -> ft.ResponsiveRow:
    """
    Displays the welcome message and the 'Open New Project' action.

    Purpose: Greets the user and provides a primary action for new projects.
    Usage: WelcomeHeaderWithNewProject(is_xs=True, on_new_project=handle_click)
    Key UI Elements: Welcome title, subtitle, OutlinedButton.
    Used In: ProjectPickView.
    """
    welcome_text = ft.Column(
        controls=[
            ft.Text(
                "Welcome back.",
                style=Styles.WELCOME_TITLE_STYLE,
                text_align=ft.TextAlign.CENTER if is_xs else ft.TextAlign.LEFT,
            ),
            ft.Text(
                "Here are your recent workspaces.",
                style=Styles.WELCOME_SUBTITLE_STYLE,
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
            style=Styles.NEW_PROJECT_BTN_STYLE,
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
def RecentProjectsList(is_xs: bool, projects: list[Project]) -> ft.Column:
    """
    Displays a column of recent project cards.

    Usage: Renders a list of projects from the state.
    Key UI Elements: RecentProjectCard instances.
    Used In: ProjectPickView.
    """
    return ft.Column(
        controls=[
            RecentProjectCard(
                project_name=project.name,
                project_path=project.path,
                updated_ago=project.updated_ago,
                show_details=not is_xs,
            )
            for project in projects
        ],
        spacing=16,
    )
