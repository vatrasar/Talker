import flet as ft

@ft.component
def PromptSettingsSidebar() -> ft.Container:
    """
    Sidebar component for prompt and whisper settings.

    Purpose: Allows the user to configure whisper language, operation mode, and target language.
    Key UI Elements: Segmented buttons for language and mode, dropdown for target language.
    Used In: PromptCreationView.
    """
    
    whisper_lang_label = ft.Text("Whisper Language", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.PRIMARY)
    whisper_lang_input = ft.SegmentedButton(
        segments=[
            ft.Segment(value="en", label=ft.Text("English"), icon=ft.Icon(ft.Icons.LANGUAGE)),
            ft.Segment(value="pl", label=ft.Text("Polish"), icon=ft.Icon(ft.Icons.LANGUAGE)),
        ],
        selected=["en"],
        allow_multiple_selection=False,
    )
    
    divider_1 = ft.Divider(height=30)
    
    op_mode_label = ft.Text("Operation Mode", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.PRIMARY)
    op_mode_input = ft.SegmentedButton(
        segments=[
            ft.Segment(value="edit", label=ft.Text("Edit"), icon=ft.Icon(ft.Icons.EDIT_NOTE)),
            ft.Segment(value="whisper", label=ft.Text("Whisper"), icon=ft.Icon(ft.Icons.MIC)),
        ],
        selected=["edit"],
        allow_multiple_selection=False,
    )
    
    divider_2 = ft.Divider(height=30)
    
    target_lang_label = ft.Text("Target Language", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.PRIMARY)
    target_lang_input = ft.Dropdown(
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

    return ft.Container(
        width=260,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=16,
        padding=20,
        content=ft.Column(
            controls=[
                whisper_lang_label,
                whisper_lang_input,
                divider_1,
                op_mode_label,
                op_mode_input,
                divider_2,
                target_lang_label,
                target_lang_input,
            ],
            spacing=10
        )
    )
