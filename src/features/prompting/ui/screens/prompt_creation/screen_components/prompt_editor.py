import flet as ft
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel


@ft.component
def PromptEditor(vm: PromptCreationViewModel) -> ft.Container:
    """
    Main editor component for creating prompts.

    Purpose: Provides text areas for source context and generated output, plus action buttons.
    Usage: Injected with PromptCreationViewModel to access project state.
    Key UI Elements: Info bar, main editing area (EditorMainArea), footer.
    Used In: PromptCreationView.
    """
    state, _ = ft.use_state(vm.state)
    page = ft.context.page

    # State for dynamic height of text fields
    min_lines, set_min_lines = ft.use_state(_calculate_min_lines(page.height))

    def handle_resize(e: ft.PageResizeEvent):
        set_min_lines(_calculate_min_lines(e.height))

    def register_resize():
        page.on_resize = handle_resize
        return lambda: setattr(page, "on_resize", None)

    ft.use_effect(register_resize, [])

    return ft.Container(
        expand=True,
        padding=ft.Padding(left=10, top=0, right=10, bottom=0),
        content=ft.Column(
            controls=[
                EditorInfoBar(vm),
                EditorMainArea(min_lines=min_lines),
                EditorFooter(),
            ],
            spacing=10,
            expand=True,
        )
    )

@ft.component
def EditorMainArea(min_lines: int) -> ft.Column:
    return ft.Column(
        controls=[
            PromptEditionSection(min_lines=min_lines),
            EditorActionCenter(),
            TranslatedPromptSection(min_lines=min_lines),
        ],
        spacing=5,
        expand=True,
    )

@ft.component
def PromptEditionSection(min_lines: int) -> ft.Column:
    text_field = ft.TextField(
        label="Source Context / Whisper Output",
        multiline=True,
        expand=False,
        min_lines=min_lines,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.Colors.OUTLINE_VARIANT,
        focused_border_color=ft.Colors.PRIMARY,
        text_size=14,
        dense=True,
    )

    return ft.Column(
        controls=[text_field],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=2,
    )

@ft.component
def TranslatedPromptSection(min_lines: int) -> ft.Column:
    text_field = ft.TextField(
        label="Generated Prompt / Translation",
        multiline=True,
        expand=False,
        min_lines=min_lines,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.Colors.OUTLINE_VARIANT,
        focused_border_color=ft.Colors.SECONDARY,
        text_size=14,
        dense=True,
    )

    return ft.Column(
        controls=[text_field],
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=2,
    )


@ft.component
def EditorInfoBar(vm: PromptCreationViewModel) -> ft.Container:
    state, _ = ft.use_state(vm.state)
    info_icon = ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=ft.Colors.PRIMARY)
    project_details = ft.Text(
        f"Project: {state.project_name} | {state.project_path}", 
        size=13, 
        weight=ft.FontWeight.W_500, 
        color=ft.Colors.ON_SURFACE_VARIANT
    )
    divider = ft.VerticalDivider()
    
    status_label = "Loading files..." if state.is_loading_files else "Ready"
    status_color = ft.Colors.PRIMARY if state.is_loading_files else ft.Colors.SECONDARY
    status_text = ft.Text(f"Status: {status_label}", size=13, color=status_color)

    return ft.Container(
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border_radius=8,
        content=ft.Row([
            info_icon,
            project_details,
            divider,
            status_text
        ])
    )

@ft.component
def EditorActionCenter() -> ft.Container:
    icon_left = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=ft.Colors.ON_PRIMARY)
    action_text = ft.Text("translate", color=ft.Colors.ON_PRIMARY, weight=ft.FontWeight.BOLD)
    icon_right = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=ft.Colors.ON_PRIMARY)
    
    action_row = ft.Row(
        controls=[icon_left, action_text, icon_right],
        tight=True,
        spacing=10,
    )
    
    action_button = ft.Container(
        content=action_row,
        padding=ft.Padding(left=25, top=12, right=25, bottom=12),
        border_radius=30,
        bgcolor=ft.Colors.PRIMARY,
        on_click=lambda _: print("Translate action"),
        shadow=ft.BoxShadow(
            blur_radius=10, 
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
        )
    )

    return ft.Container(
        expand=1,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[action_button]
        ),
    )

@ft.component
def EditorFooter() -> ft.Row:
    copy_btn = ft.Button(
        "Copy to Clipboard",
        icon=ft.Icons.CONTENT_COPY_ROUNDED,
        style=ft.ButtonStyle(
            color=ft.Colors.ON_SECONDARY_CONTAINER,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=20,
        ),
        on_click=lambda _: print("Copy to clipboard")
    )

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[copy_btn]
    )

def _calculate_min_lines(height: float) -> int:
    if height < 600:
        return 2
    if height < 900:
        return 8
    return 12
