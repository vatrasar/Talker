import flet as ft
from typing import Callable
from features.landing.ui.screens.project_pick.screen_styles.project_pick_styles import ProjectPickStyles as Styles


@ft.component
def RecentProjectCard(
    project_name: str,
    project_path: str,
    updated_ago: str,
    show_details: bool = True,
    on_click: Callable[[], None] | None = None,
):
    """
    Displays a brief summary of a recently opened project.

    Purpose: To allow users to select and open a recent project from the landing screen.
    Usage:
        RecentProjectCard(
            project_name="AI Marketing Research",
            project_path="/Users/admin/Documents/...",
            updated_ago="Updated 2h ago",
            on_click=handle_project_click
        )
    Key UI Elements: Folder icon, project name text, project path text, last updated text, menu icon.
    Used In: RecentProjectsList.
    """
    is_hovered, set_is_hovered = ft.use_state(False)

    def handle_click(e: ft.ControlEvent) -> None:
        if on_click:
            on_click()

    def handle_hover(e: ft.ControlEvent) -> None:
        set_is_hovered(e.data)

    def handle_more_options(e: ft.ControlEvent) -> None:
        pass

    return ft.Container(
        key=f"recent_project_card_{project_path}",
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH if is_hovered else ft.Colors.SURFACE_CONTAINER,
        border_radius=Styles.CARD_BORDER_RADIUS,
        padding=ft.Padding.all(20),
        border=ft.Border.all(1, ft.Colors.PRIMARY if is_hovered else ft.Colors.OUTLINE_VARIANT),
        on_click=handle_click,
        on_hover=handle_hover,
        animate=Styles.CARD_ANIMATION,
        scale=1.01 if is_hovered else 1.0,
        content=ft.Row(
            controls=[
                ProjectIcon(),
                ProjectInfo(name=project_name, path=project_path),
                UpdatedTimestamp(text=updated_ago, visible=show_details),
                MoreOptionsButton(on_click=handle_more_options),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )


# --- Sub-components (Implementation Details) ---


@ft.component
def ProjectIcon():
    """Displays the visual icon representing a project folder."""
    return ft.Container(
        content=ft.Icon(ft.Icons.FOLDER_OUTLINED, color=ft.Colors.PRIMARY, size=24),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        width=48,
        height=48,
        alignment=ft.Alignment.CENTER,
        border_radius=Styles.CARD_BORDER_RADIUS,
    )


@ft.component
def ProjectInfo(name: str, path: str):
    """Displays the project's name and its file path location."""
    return ft.Column(
        controls=[
            ft.Text(
                name,
                style=Styles.CARD_NAME_STYLE,
            ),
            ft.Text(
                path,
                style=Styles.CARD_PATH_STYLE,
                overflow=ft.TextOverflow.ELLIPSIS,
                max_lines=1,
            ),
        ],
        expand=True,
        spacing=4,
    )


@ft.component
def UpdatedTimestamp(text: str, visible: bool):
    """Displays the time elapsed since the project was last modified."""
    return ft.Text(
        text,
        style=Styles.CARD_TIMESTAMP_STYLE,
        visible=visible,
    )


@ft.component
def MoreOptionsButton(on_click: Callable[[ft.ControlEvent], None]):
    """Icon button for accessing contextual actions for the project."""
    return ft.IconButton(
        icon=ft.Icons.MORE_HORIZ,
        icon_color=ft.Colors.ON_SURFACE_VARIANT,
        tooltip="More Options",
        on_click=on_click,
    )
