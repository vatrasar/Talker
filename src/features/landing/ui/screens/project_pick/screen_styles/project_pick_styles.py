import flet as ft


class ProjectPickStyles:
    """Styles and constants for the ProjectPick screen."""

    # Logo Section
    LOGO_TEXT_STYLE = ft.TextStyle(
        size=40,
        weight=ft.FontWeight.W_900,
        color=ft.Colors.PRIMARY,
        letter_spacing=-1,
    )

    # Welcome Header
    WELCOME_TITLE_STYLE = ft.TextStyle(
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.ON_SURFACE,
    )
    WELCOME_SUBTITLE_STYLE = ft.TextStyle(
        size=14,
        color=ft.Colors.ON_SURFACE_VARIANT,
    )

    # New Project Button
    NEW_PROJECT_BTN_STYLE = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=4),
        side=ft.BorderSide(1, ft.Colors.OUTLINE),
        padding=ft.Padding.all(16),
        bgcolor=ft.Colors.SURFACE_CONTAINER,
    )

    # Recent Project Card
    CARD_BORDER_RADIUS = 8
    CARD_ANIMATION = ft.Animation(200, ft.AnimationCurve.EASE_OUT)

    # Project Card Sub-components
    CARD_NAME_STYLE = ft.TextStyle(
        weight=ft.FontWeight.BOLD,
        size=16,
        color=ft.Colors.ON_SURFACE,
    )
    CARD_PATH_STYLE = ft.TextStyle(
        size=12,
        color=ft.Colors.ON_SURFACE_VARIANT,
    )
    CARD_TIMESTAMP_STYLE = ft.TextStyle(
        size=12,
        color=ft.Colors.ON_SURFACE_VARIANT,
    )
