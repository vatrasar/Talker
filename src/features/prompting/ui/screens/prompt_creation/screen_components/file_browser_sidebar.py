import flet as ft

@ft.component
def FileBrowserSidebar() -> ft.Container:
    """
    Sidebar component for browsing project files.

    Purpose: Displays a tree structure of the current project's files and folders.
    Key UI Elements: Folder tree with expansion tiles.
    Used In: PromptCreationView.
    """
    
    def folder_item(name: str, children: list = None):
        if children:
            return ft.ExpansionTile(
                leading=ft.Icon(
                    ft.Icons.FOLDER_OPEN if children else ft.Icons.FOLDER, 
                    color=ft.Colors.PRIMARY,
                    size=20
                ),
                title=ft.Text(name, size=14),
                affinity=ft.TileAffinity.LEADING,
                trailing=ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=20, color=ft.Colors.PRIMARY_CONTAINER),
                collapsed_text_color=ft.Colors.ON_SURFACE,
                text_color=ft.Colors.PRIMARY,
                controls=children,
                controls_padding=ft.Padding(left=20),
                dense=True,
            )
        return ft.ListTile(
            leading=ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED, size=20, color=ft.Colors.OUTLINE),
            title=ft.Text(name, size=14),
            dense=True,
        )

    hardcoded_tree = [
        folder_item("src", children=[
            folder_item("features", children=[
                folder_item("prompting", children=[
                    folder_item("ui", children=[
                        folder_item("prompt_creation_view.py")
                    ])
                ])
            ]),
            folder_item("main.py")
        ]),
        folder_item("requirements.txt"),
        folder_item("README.md")
    ]

    return ft.Container(
        width=280,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=16,
        padding=15,
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_TREE_ROUNDED, color=ft.Colors.PRIMARY),
                    ft.Text("Project Files", weight=ft.FontWeight.BOLD, size=18),
                ]),
                ft.Divider(height=20, thickness=1),
                ft.Column(
                    controls=hardcoded_tree,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=0
                )
            ],
            expand=True
        )
    )
