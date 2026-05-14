import flet as ft
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel

@ft.component
def PromptEditor(vm: PromptCreationViewModel) -> ft.Container:
    """
    Main editor component for creating prompts.

    Purpose: Provides text areas for source context and generated output, plus action buttons.
    Usage: Injected with PromptCreationViewModel to access project state.
    Key UI Elements: Info bar, source text field, action center, result text field, footer.
    Used In: PromptCreationView.
    """
    state, _ = ft.use_state(vm.state)

    return ft.Container(
        expand=True,
        padding=ft.Padding(left=10, top=0, right=10, bottom=0),
        content=ft.Column(
            controls=[
                EditorInfoBar(state.project_name, state.project_path),
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
                EditorActionCenter(),
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
                EditorFooter(),
            ],
            spacing=15
        )
    )

@ft.component
def EditorInfoBar(project_name: str, project_path: str) -> ft.Container:
    """
    Displays the current project's name and path.

    Purpose: Provide context about the active project within the editor.
    Key UI Elements: Info icon, project metadata, status indicator.
    Used In: PromptEditor.
    """
    return ft.Container(
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border_radius=8,
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=ft.Colors.PRIMARY),
            ft.Text(
                f"Project: {project_name} | {project_path}", 
                size=13, 
                weight=ft.FontWeight.W_500, 
                color=ft.Colors.ON_SURFACE_VARIANT
            ),
            ft.VerticalDivider(),
            ft.Text("Status: Ready", size=13, color=ft.Colors.SECONDARY)
        ])
    )

@ft.component
def EditorActionCenter() -> ft.Row:
    """
    Center action controls for prompt generation.

    Purpose: Contains the primary trigger for translating or generating content.
    Key UI Elements: Floating action-style IconButton.
    Used In: PromptEditor.
    """
    return ft.Row(
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
                padding=5,
                shape=ft.BoxShape.CIRCLE,
                shadow=ft.BoxShadow(
                    blur_radius=10, 
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
                )
            )
        ]
    )

@ft.component
def EditorFooter() -> ft.Row:
    """
    Bottom action bar for secondary editor operations.

    Purpose: Provides copy and other utility actions.
    Key UI Elements: Copy to clipboard button.
    Used In: PromptEditor.
    """
    return ft.Row(
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
