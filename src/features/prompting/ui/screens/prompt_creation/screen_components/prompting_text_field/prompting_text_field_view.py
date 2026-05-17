import flet as ft
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType

@ft.component
def PromptingTextField(
    label: str,
    min_lines: int = 5,
) -> ft.Container:
    """
    Custom simulated text field that displays prompt items from PromptingCreationService.

    Purpose: Renders single words as text blocks and filesystem items as premium button chips,
             wrapping beautifully, and focusing the end input field upon clicking the component.
    Usage: Implemented inside PromptEditionSection as a replacement for standard text field.
    Key UI Elements: Wrapping flow list of words/chips, borderless trailing textfield,
                     position-animated label.
    Used In: PromptEditionSection.
    """
    di = ft.context.page.session.store.get("di_container")
    vm = ft.use_memo(di.build_prompting_text_field_view_model, [])
    state, _ = ft.use_state(vm.state)

    is_focused, set_is_focused = ft.use_state(False)
    is_hovered, set_is_hovered = ft.use_state(False)

    textfield_ref = ft.Ref[ft.TextField]()

    def sync_props() -> None:
        vm.update_props(label=label)

    ft.use_effect(sync_props, [label])

    async def handle_focus(e: ft.ControlEvent) -> None:
        set_is_focused(True)
        await vm.handle_focus()

    async def handle_blur(e: ft.ControlEvent) -> None:
        set_is_focused(False)
        await vm.finish_editing()

    async def handle_change(e: ft.ControlEvent) -> None:
        vm.update_text(e.control.value)

    async def handle_hover(e: ft.HoverEvent) -> None:
        set_is_hovered(e.data)

    async def handle_label_click(e: ft.ControlEvent) -> None:
        if textfield_ref.current:
            await textfield_ref.current.focus()
            

    is_active = is_focused or bool(state.value) or bool(state.items)

    border_color = (
        ft.Colors.PRIMARY
        if is_focused
        else (ft.Colors.OUTLINE if is_hovered else ft.Colors.OUTLINE_VARIANT)
    )
    border_width = 2 if is_focused else 1

    border = ft.Border.all(width=border_width, color=border_color)

    prompt_controls = []
    for item in state.items:
        if isinstance(item.value, str):
            prompt_controls.append(
                ft.Text(
                    key=f"prompt_word_{item.index}",
                    value=item.value,
                    size=14,
                    color=ft.Colors.ON_SURFACE,
                )
            )
        else:
            item_val = item.value
            icon_name = (
                ft.Icons.FOLDER_ROUNDED
                if item_val.type == FileSystemItemType.FOLDER
                else ft.Icons.INSERT_DRIVE_FILE_ROUNDED
            )
            prompt_controls.append(
                ft.Container(
                    key=f"prompt_file_{item_val.path}",
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon_name, size=16, color=ft.Colors.ON_SECONDARY_CONTAINER),
                            ft.Text(
                                value=item_val.name,
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.ON_SECONDARY_CONTAINER,
                            ),
                        ],
                        tight=True,
                        spacing=4,
                    ),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    padding=ft.Padding(12, 6, 12, 6),
                    border_radius=ft.BorderRadius.all(16),
                    border=ft.Border.all(width=1, color=ft.Colors.OUTLINE_VARIANT),
                )
            )

    textfield = ft.TextField(
        key="prompt_editing_textfield",
        ref=textfield_ref,
        value=state.value,
        multiline=True,
        width=200,
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(0, 0, 0, 0),
        text_size=14,
        on_focus=handle_focus,
        on_blur=handle_blur,
        on_change=handle_change,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
        autofocus=is_focused,
    )

    inner_content = ft.Container(
        content=ft.Row(
            controls=prompt_controls + [textfield],
            wrap=True,
            spacing=8,
            run_spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(16, 16, 16, 16),
        on_click=handle_label_click,
    )

    border_container = ft.Container(
        content=inner_content,
        border=border,
        border_radius=ft.BorderRadius.all(8),
        bgcolor=ft.Colors.SURFACE,
        top=10,
        bottom=0,
        left=0,
        right=0,
        on_hover=handle_hover,
        on_click=handle_label_click,
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )

    label_text = ft.Text(
        value=state.label,
        size=14,
        color=ft.Colors.PRIMARY if is_focused else ft.Colors.ON_SURFACE_VARIANT,
    )

    label_container = ft.Container(
        content=label_text,
        top=0 if is_active else 28,
        left=12 if is_active else 16,
        scale=0.85 if is_active else 1.0,
        animate_position=ft.Animation(180, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_scale=ft.Animation(180, ft.AnimationCurve.EASE_OUT_CUBIC),
        bgcolor=ft.Colors.SURFACE if is_active else ft.Colors.TRANSPARENT,
        padding=ft.Padding(4, 0, 4, 0) if is_active else ft.Padding(0, 0, 0, 0),
        on_click=handle_label_click,
    )

    stack = ft.Stack(
        controls=[
            border_container,
            label_container,
        ],
        expand=True,
        clip_behavior=ft.ClipBehavior.NONE,
    )

    height = min_lines * 20 + 38 + 10
    if len(state.items) > 0:
        height += 30

    return ft.Container(
        content=stack,
        bgcolor=ft.Colors.TRANSPARENT,
        height=height,
        clip_behavior=ft.ClipBehavior.NONE,
        on_click=handle_label_click,
    )
