import flet as ft
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel

@ft.component
def PromptEditor(vm: PromptCreationViewModel) -> ft.Container:
    """
    Main editor component for creating prompts.

    Purpose: Provides text areas for source context and generated output, plus action buttons.
    Key UI Elements: Info bar, text fields, translate button, footer actions.
    Used In: PromptCreationView.
    """
    state, _ = ft.use_state(vm.state)

    return ft.Container(
        expand=True,
        padding=ft.Padding(left=10, top=0, right=10, bottom=0),
        content=ft.Column(
            controls=[
                # Status/Info Bar
                ft.Container(
                    padding=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border_radius=8,
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=ft.Colors.PRIMARY),
                        ft.Text(f"Project: {state.project_name} | {state.project_path}", 
                                size=13, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE_VARIANT),
                        ft.VerticalDivider(),
                        ft.Text("Status: Ready", size=13, color=ft.Colors.SECONDARY)
                    ])
                ),
                
                # Top Text Field
                ft.TextField(
                    label="Source Context / Whisper Output",
                    multiline=True,
                    expand=True,
                    min_lines=8,
                    border=ft.InputBorder.OUTLINE,
                    border_color=ft.Colors.OUTLINE_VARIANT,
                    focused_border_color=ft.Colors.PRIMARY,
                    text_size=14,
                ),
                
                # Action Center
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.TRANSLATE_ROUNDED,
                                icon_size=32,
                                icon_color=ft.Colors.ON_PRIMARY,
                                bgcolor=ft.Colors.PRIMARY,
                                tooltip="Generate / Translate",
                                on_click=lambda _: print("Translate action")
                            ),
                            padding=ft.Padding(5, 5, 5, 5),
                            shape=ft.BoxShape.CIRCLE,
                            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK))
                        )
                    ]
                ),
                
                # Bottom Text Field
                ft.TextField(
                    label="Generated Prompt / Translation",
                    multiline=True,
                    expand=True,
                    min_lines=8,
                    border=ft.InputBorder.OUTLINE,
                    border_color=ft.Colors.OUTLINE_VARIANT,
                    focused_border_color=ft.Colors.SECONDARY,
                    text_size=14,
                ),
                
                # Footer Actions
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(
                            "Copy to Clipboard",
                            icon=ft.Icons.CONTENT_COPY_ROUNDED,
                            style=ft.ButtonStyle(
                                color=ft.Colors.ON_SECONDARY_CONTAINER,
                                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                                padding=20,
                            ),
                            on_click=lambda _: print("Copy to clipboard")
                        )
                    ]
                )
            ],
            spacing=15
        )
    )
