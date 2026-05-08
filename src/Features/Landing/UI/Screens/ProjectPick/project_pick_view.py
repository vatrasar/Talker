import flet as ft
from Features.Landing.UI.Screens.ProjectPick.ScreenComponents.recent_project_card import RecentProjectCard

class ProjectPickView(ft.View):
    """
    The initial landing screen of the application.
    
    Purpose: Provides the user with options to open existing projects or create a new one.
    Available Functionalities: View recent projects list, navigate to new project creation.
    Key UI Elements: Application logo, welcome header, "Open New Project" button, list of recent projects.
    Navigate From: App Launch
    Navigate To: Feature-specific screens (e.g., Workspace) depending on the selected project.
    """

    def __init__(self, route: str = "/") -> None:
        super().__init__(route=route)
        
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 0
        self.scroll = ft.ScrollMode.AUTO
        
        self._build_ui()

    def _build_ui(self) -> None:
        logo_row = ft.Row(
            controls=[
                ft.Icon(ft.Icons.BAR_CHART, color=ft.Colors.PRIMARY, size=48),
                ft.Text("Talker", size=40, weight=ft.FontWeight.W_900, color=ft.Colors.PRIMARY, style=ft.TextStyle(letter_spacing=-1))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        header_row = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Welcome back.", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE),
                        ft.Text("Here are your recent workspaces.", size=14, color=ft.Colors.ON_SURFACE_VARIANT)
                    ],
                    spacing=4
                ),
                ft.OutlinedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CREATE_NEW_FOLDER_OUTLINED, size=18, color=ft.Colors.PRIMARY),
                            ft.Text("Open New Project", size=14, color=ft.Colors.PRIMARY, weight=ft.FontWeight.W_500)
                        ],
                        spacing=8
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=4),
                        side=ft.BorderSide(1, ft.Colors.OUTLINE),
                        padding=ft.Padding.all(16),
                        bgcolor=ft.Colors.SURFACE_CONTAINER
                    ),
                    on_click=self._handle_new_project
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END
        )
        
        divider = ft.Divider(height=40, color=ft.Colors.OUTLINE_VARIANT)
        
        projects_column = ft.Column(
            controls=[
                RecentProjectCard(
                    project_name="AI Marketing Research",
                    project_path="/Users/admin/Documents/Talker/AI-Marketing-Research",
                    updated_ago="Updated 2h ago"
                ),
                RecentProjectCard(
                    project_name="Global Expansion Strategy",
                    project_path="C:\\Projects\\Global-Strategy",
                    updated_ago="Updated 1d ago"
                ),
                RecentProjectCard(
                    project_name="Q3 Financials",
                    project_path="/Volumes/Data/Finance/Q3-2024",
                    updated_ago="Updated 3d ago"
                ),
                RecentProjectCard(
                    project_name="Product Launch Rev 2",
                    project_path="D:\\Work\\Talker\\Launch-Rev2",
                    updated_ago="Updated 1w ago"
                ),
                RecentProjectCard(
                    project_name="Social Media Campaign",
                    project_path="/Users/admin/Projects/Social-Media",
                    updated_ago="Updated 2w ago"
                ),
                RecentProjectCard(
                    project_name="Brand Identity Refresh",
                    project_path="C:\\Designs\\Brand-Refresh",
                    updated_ago="Updated 3w ago"
                ),
                RecentProjectCard(
                    project_name="Market Analysis 2024",
                    project_path="/Volumes/Data/Reports/Market-Analysis",
                    updated_ago="Updated 1m ago"
                ),
                RecentProjectCard(
                    project_name="Investor Pitch Deck",
                    project_path="/Users/admin/Documents/Pitch-Deck",
                    updated_ago="Updated 2m ago"
                )
            ],
            spacing=16
        )
        
        self.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(content=logo_row, margin=ft.Margin.only(bottom=80)),
                        header_row,
                        divider,
                        projects_column
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH
                ),
                padding=ft.Padding.symmetric(horizontal=200, vertical=60)
            )
        )

    def _handle_new_project(self, e: ft.ControlEvent) -> None:
        pass
