import flet as ft
from typing import Callable

class RecentProjectCard(ft.Container):
    """
    Displays a brief summary of a recently opened project.
    
    Purpose: To allow users to select and open a recent project from the landing screen.
    Usage:
        RecentProjectCard(
            project_name="AI Marketing Research",
            project_path="/Users/admin/Documents/...",
            updated_ago="Updated 2h ago",
            on_click=self.handle_project_click
        )
    Key UI Elements: Folder icon, project name text, project path text, last updated text, menu icon.
    Used In: ProjectPickView
    """

    def __init__(
        self,
        project_name: str,
        project_path: str,
        updated_ago: str,
        on_click: Callable[[], None] | None = None
    ) -> None:
        super().__init__()
        
        self.project_name: str = project_name
        self.project_path: str = project_path
        self.updated_ago: str = updated_ago
        self._on_click_callback: Callable[[], None] | None = on_click
        
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.border_radius = 8
        self.padding = ft.Padding.all(20)
        self.border = ft.Border.all(1, ft.Colors.OUTLINE_VARIANT)
        self.on_click = self._handle_click
        self.on_hover = self._handle_hover
        
        # Hover animations
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        self.scale = 1.0
        
        self.content = ft.Row(
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
                        ft.Text(self.project_name, weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.ON_SURFACE),
                        ft.Text(self.project_path, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                    expand=True,
                    spacing=4,
                ),
                ft.Text(self.updated_ago, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.IconButton(
                    icon=ft.Icons.MORE_HORIZ,
                    icon_color=ft.Colors.ON_SURFACE_VARIANT,
                    tooltip="More Options",
                    on_click=self._handle_more_options
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        if self._on_click_callback:
            self._on_click_callback()

    def _handle_hover(self, e: ft.ControlEvent) -> None:
        is_hovered = e.data
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGH if is_hovered else ft.Colors.SURFACE_CONTAINER
        self.border = ft.Border.all(1, ft.Colors.PRIMARY if is_hovered else ft.Colors.OUTLINE_VARIANT)
        self.scale = 1.01 if is_hovered else 1.0
        self.update()

    def _handle_more_options(self, e: ft.ControlEvent) -> None:
        pass
