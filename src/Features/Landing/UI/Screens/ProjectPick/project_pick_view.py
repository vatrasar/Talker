import flet as ft

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

    logo_row = ft.Row(
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
    )

    welcome_messages = ft.Column(
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

    new_project_button = ft.OutlinedButton(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                    size=18,
                    color=ft.Colors.PRIMARY,
                ),
                ft.Text(
                    "Open New Project",
                    size=14,
                    color=ft.Colors.PRIMARY,
                    weight=ft.FontWeight.W_500,
                ),
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
        on_click=handle_new_project,
    )

    new_project_action = ft.Container(
        content=new_project_button,
        col={"xs": 12, "sm": 4, "md": 4},
        alignment=ft.Alignment.CENTER if is_xs else ft.Alignment.CENTER_RIGHT,
    )

    header_row = ft.ResponsiveRow(
        controls=[
            welcome_messages,
            new_project_action,
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    divider = ft.Divider(height=40, color=ft.Colors.OUTLINE_VARIANT)

    projects_column = ft.Column(
        controls=[
            RecentProjectCard(
                project_name="AI Marketing Research",
                project_path="/Users/admin/Documents/Talker/AI-Marketing-Research",
                updated_ago="Updated 2h ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Global Expansion Strategy",
                project_path="C:\\Projects\\Global-Strategy",
                updated_ago="Updated 1d ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Q3 Financials",
                project_path="/Volumes/Data/Finance/Q3-2024",
                updated_ago="Updated 3d ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Product Launch Rev 2",
                project_path="D:\\Work\\Talker\\Launch-Rev2",
                updated_ago="Updated 1w ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Social Media Campaign",
                project_path="/Users/admin/Projects/Social-Media",
                updated_ago="Updated 2w ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Brand Identity Refresh",
                project_path="C:\\Designs\\Brand-Refresh",
                updated_ago="Updated 3w ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Market Analysis 2024",
                project_path="/Volumes/Data/Reports/Market-Analysis",
                updated_ago="Updated 1m ago",
                show_details=not is_xs,
            ),
            RecentProjectCard(
                project_name="Investor Pitch Deck",
                project_path="/Users/admin/Documents/Pitch-Deck",
                updated_ago="Updated 2m ago",
                show_details=not is_xs,
            ),
        ],
        spacing=16,
    )

    main_content_column = ft.Column(
        col={"xs": 12, "sm": 10, "md": 10, "lg": 8, "xl": 8},
        offset={"sm": 1, "md": 1, "lg": 2, "xl": 2},
        controls=[
            ft.Container(
                content=logo_row,
                margin=ft.Margin.only(bottom=80),
                alignment=ft.Alignment.CENTER,
            ),
            header_row,
            divider,
            projects_column,
        ],
        spacing=10,
    )

    return ft.Container(
        content=ft.ListView(
            controls=[
                ft.ResponsiveRow(
                    controls=[main_content_column],
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
