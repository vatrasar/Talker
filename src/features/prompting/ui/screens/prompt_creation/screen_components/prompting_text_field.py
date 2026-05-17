import flet as ft
from typing import Callable, Any, Optional

@ft.component
def PromptingTextField(
    label: str,
    value: str = "",
    on_change: Optional[Callable[[ft.ControlEvent], Any]] = None,
    min_lines: int = 5,
) -> ft.Container:
    """
    Custom simulated text field with premium focus and floating label transitions.

    Purpose: Simulates a native outlined text field with a floating label that shrinks 
             and blends into the top border when focused or non-empty.
    Usage: Implemented inside PromptEditionSection as a replacement for standard text field.
    Key UI Elements: Animated container border, borderless text field, animated positioned 
                     label container with background masking.
    Used In: PromptEditionSection.
    """
    is_focused, set_is_focused = ft.use_state(False)
    is_hovered, set_is_hovered = ft.use_state(False)
    current_value, set_current_value = ft.use_state(value)
    
    textfield_ref = ft.Ref[ft.TextField]()

    def sync_props():
        set_current_value(value)

    ft.use_effect(sync_props, [value])

    def handle_focus(e: ft.ControlEvent):
        set_is_focused(True)

    def handle_blur(e: ft.ControlEvent):
        set_is_focused(False)

    def handle_change(e: ft.ControlEvent):
        set_current_value(e.control.value)
        if on_change:
            on_change(e)

    def handle_hover(e: ft.HoverEvent):
        set_is_hovered(e.data)

    async def handle_label_click(e: ft.ControlEvent):
        if textfield_ref.current:
            await textfield_ref.current.focus()

    is_active = is_focused or bool(current_value)

    border_color = (
        ft.Colors.PRIMARY
        if is_focused
        else (ft.Colors.OUTLINE if is_hovered else ft.Colors.OUTLINE_VARIANT)
    )
    border_width = 2 if is_focused else 1

    border = ft.Border.all(width=border_width, color=border_color)
    
    textfield = ft.TextField(
        ref=textfield_ref,
        value=current_value,
        multiline=True,
        expand=True,
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(16, 16, 16, 16),
        text_size=14,
        on_focus=handle_focus,
        on_blur=handle_blur,
        on_change=handle_change,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
    )

    border_container = ft.Container(
        content=textfield,
        border=border,
        border_radius=ft.BorderRadius.all(8),
        bgcolor=ft.Colors.SURFACE,
        top=10,
        bottom=0,
        left=0,
        right=0,
        on_hover=handle_hover,
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )

    label_text = ft.Text(
        value=label,
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

    return ft.Container(
        content=stack,
        bgcolor=ft.Colors.TRANSPARENT,
        height=height,
        clip_behavior=ft.ClipBehavior.NONE,
    )
