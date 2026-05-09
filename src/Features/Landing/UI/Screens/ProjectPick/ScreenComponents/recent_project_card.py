import flet as ft
from typing import Callable


@ft.component
def RecentProjectCard(
    project_name: str,
    project_path: str,
    updated_ago: str,
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
    Used In: ProjectPickView
    """
    is_hovered, set_is_hovered = ft.use_state(False)

    def handle_click(e: ft.ControlEvent) -> None:
        if on_click:
            on_click()

    def handle_hover(e: ft.ControlEvent) -> None:
        set_is_hovered(str(e.data).lower() == "true")

    def handle_more_options(e: ft.ControlEvent) -> None:
        pass

    return ft.Container(
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH if is_hovered else ft.Colors.SURFACE_CONTAINER,
        border_radius=8,
        padding=ft.Padding.all(20),
        border=ft.Border.all(1, ft.Colors.PRIMARY if is_hovered else ft.Colors.OUTLINE_VARIANT),
        on_click=handle_click,
        on_hover=handle_hover,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        scale=1.01 if is_hovered else 1.0,
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.FOLDER_OUTLINED, color=ft.Colors.PRIMARY, size=24),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                    width=48,
                    height=48,
                    alignment=ft.Alignment(0, 0),
                    border_radius=8,
                ),
                ft.Column(
                    controls=[
                        ft.Text(project_name, weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.ON_SURFACE),
                        ft.Text(project_path, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                    expand=True,
                    spacing=4,
                ),
                ft.Text(updated_ago, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.IconButton(
                    icon=ft.Icons.MORE_HORIZ,
                    icon_color=ft.Colors.ON_SURFACE_VARIANT,
                    tooltip="More Options",
                    on_click=handle_more_options,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
    )
