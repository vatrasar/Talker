import asyncio
import urllib.parse
import flet as ft
from typing import Any, Callable

from features.landing.ui.screens.project_pick.screen_components.recent_project_card import RecentProjectCard
from features.landing.ui.screens.project_pick.screen_styles.project_pick_styles import ProjectPickStyles as Styles
from features.landing.ui.screens.project_pick.project_pick_view_model import ProjectPickViewModel
from features.landing.domain.models.project import Project
from features.prompting.prompting_routes import PROMPT_CREATION_ROUTE


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
    di = page.session.store.get("di_container")
    vm: ProjectPickViewModel = ft.use_memo(di.build_project_pick_view_model, [])
    state, _ = ft.use_state(vm.state)
    
    is_xs, set_is_xs = ft.use_state(page.width < 576)
    file_picker = ft.use_memo(ft.FilePicker, [])

    def register_file_picker():
        page.services.append(file_picker)
        return lambda: page.services.remove(file_picker)

    ft.use_effect(register_file_picker, [])

    async def load_projects() -> None:
        await vm.load_recent_projects()

    def on_mount():
        page.run_task(load_projects)

    ft.use_effect(on_mount, [])

    async def handle_new_project_click(e: ft.ControlEvent) -> None:
        path = await file_picker.get_directory_path()
        if path:
            await vm.handle_folder_selected(path)


    def handle_resize(e: ft.ControlEvent) -> None:
        set_is_xs(page.width < 576)

    def register_resize():
        page.on_resize = handle_resize
        return lambda: setattr(page, "on_resize", None)

    ft.use_effect(register_resize, [])

    main_content_column = ft.Column(
        col={"xs": 12, "sm": 10, "md": 10, "lg": 8, "xl": 8},
        offset={"sm": 1, "md": 1, "lg": 2, "xl": 2},
        controls=[
            LogoSection(),
            WelcomeHeaderWithNewProject(is_xs=is_xs, on_new_project=handle_new_project_click),
            ft.Divider(height=40, color=ft.Colors.OUTLINE_VARIANT),
            RecentProjectsList(is_xs=is_xs, projects=state.projects),
        ],
        spacing=10,
    )
    
    responsive_container = ft.ResponsiveRow(
        controls=[main_content_column],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    list_view = ft.ListView(
        controls=[responsive_container],
        spacing=10,
        padding=ft.Padding.symmetric(horizontal=20),
    )

    return ft.Container(
        content=list_view,
        bgcolor=ft.Colors.SURFACE,
        padding=ft.Padding.symmetric(vertical=60),
        expand=True,
    )


@ft.component
def LogoSection() -> ft.Container:
    chart_icon = ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.PRIMARY, size=48)
    app_title = ft.Text(
        "Talker",
        style=Styles.LOGO_TEXT_STYLE,
    )
    
    logo_row = ft.Row(
        controls=[chart_icon, app_title],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
    )

    return ft.Container(
        content=logo_row,
        margin=ft.Margin.only(bottom=80),
        alignment=ft.Alignment.CENTER,
    )


@ft.component
def WelcomeHeaderWithNewProject(is_xs: bool, on_new_project: Callable[[ft.ControlEvent], Any]) -> ft.ResponsiveRow:
    return ft.ResponsiveRow(
        controls=[
            WelcomeText(is_xs=is_xs),
            NewProjectButton(is_xs=is_xs, on_new_project=on_new_project),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def WelcomeText(is_xs: bool) -> ft.Column:
    welcome_title = ft.Text(
        "Welcome back.",
        style=Styles.WELCOME_TITLE_STYLE,
        text_align=ft.TextAlign.CENTER if is_xs else ft.TextAlign.LEFT,
    )
    
    welcome_subtitle = ft.Text(
        "Here are your recent workspaces.",
        style=Styles.WELCOME_SUBTITLE_STYLE,
        text_align=ft.TextAlign.CENTER if is_xs else ft.TextAlign.LEFT,
    )

    return ft.Column(
        controls=[welcome_title, welcome_subtitle],
        col={"xs": 12, "sm": 8, "md": 8},
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER if is_xs else ft.CrossAxisAlignment.START,
    )


@ft.component
def NewProjectButton(is_xs: bool, on_new_project: Callable[[ft.ControlEvent], Any]) -> ft.Container:
    folder_icon = ft.Icon(ft.Icons.CREATE_NEW_FOLDER_OUTLINED, size=18, color=ft.Colors.PRIMARY)
    button_text = ft.Text("Open New Project", size=14, color=ft.Colors.PRIMARY, weight=ft.FontWeight.W_500)
    
    button_content_row = ft.Row(
        controls=[folder_icon, button_text],
        spacing=8,
        tight=True,
    )
    
    outlined_button = ft.OutlinedButton(
        content=button_content_row,
        style=Styles.NEW_PROJECT_BTN_STYLE,
        on_click=on_new_project,
    )

    return ft.Container(
        content=outlined_button,
        col={"xs": 12, "sm": 4, "md": 4},
        alignment=ft.Alignment.CENTER if is_xs else ft.Alignment.CENTER_RIGHT,
    )


@ft.component
def RecentProjectsList(is_xs: bool, projects: list[Project]) -> ft.Column:
    if not projects:
        empty_icon = ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED, size=40, color=ft.Colors.OUTLINE)
        empty_text = ft.Text(
            "No recent projects yet.\nOpen a folder to get started.",
            style=Styles.WELCOME_SUBTITLE_STYLE,
            text_align=ft.TextAlign.CENTER,
        )
        
        empty_column = ft.Column(
            controls=[empty_icon, empty_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        empty_container = ft.Container(
            content=empty_column,
            padding=ft.Padding.symmetric(vertical=40),
            alignment=ft.Alignment.CENTER,
        )

        return ft.Column(
            controls=[empty_container]
        )

    return ft.Column(
        controls=[
            RecentProjectCard(
                project_name=project.name,
                project_path=project.path,
                updated_ago=project.updated_ago,
                show_details=not is_xs,
                on_click=lambda p=project: ft.context.page.navigate(
                    f"/prompts/create/{urllib.parse.quote(p.name, safe='')}/{urllib.parse.quote(p.path, safe='')}"
                ),
            )
            for project in projects
        ],
        spacing=16,
    )
