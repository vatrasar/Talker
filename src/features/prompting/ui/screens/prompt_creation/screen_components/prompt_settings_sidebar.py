import flet as ft

@ft.component
def PromptSettingsSidebar() -> ft.Container:
    """
    Sidebar component for prompt and whisper settings.

    Purpose: Allows the user to configure whisper language, operation mode, and target language.
    Key UI Elements: Segmented buttons for language and mode, dropdown for target language.
    Used In: PromptCreationView.
    """
    
    return ft.Container(
        width=260,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=16,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Whisper Language", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.PRIMARY),
                ft.SegmentedButton(
                    segments=[
                        ft.Segment(value="en", label=ft.Text("English"), icon=ft.Icon(ft.Icons.LANGUAGE)),
                        ft.Segment(value="pl", label=ft.Text("Polish"), icon=ft.Icon(ft.Icons.LANGUAGE)),
                    ],
                    selected=["en"],
                    allow_multiple_selection=False,
                ),
                
                ft.Divider(height=30),
                
                ft.Text("Operation Mode", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.PRIMARY),
                ft.SegmentedButton(
                    segments=[
                        ft.Segment(value="edit", label=ft.Text("Edit"), icon=ft.Icon(ft.Icons.EDIT_NOTE)),
                        ft.Segment(value="whisper", label=ft.Text("Whisper"), icon=ft.Icon(ft.Icons.MIC)),
                    ],
                    selected=["edit"],
                    allow_multiple_selection=False,
                ),
                
                ft.Divider(height=30),
                
                ft.Text("Target Language", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.PRIMARY),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("English"),
                        ft.dropdown.Option("Polish"),
                        ft.dropdown.Option("Spanish"),
                        ft.dropdown.Option("French"),
                    ],
                    value="English",
                    border_radius=10,
                    content_padding=10,
                )
            ],
            spacing=10
        )
    )
