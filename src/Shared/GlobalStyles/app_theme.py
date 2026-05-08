import flet as ft

def get_app_theme() -> ft.Theme:
    """
    Returns the global application theme based on the Talker Design System.
    
    Includes color scheme, typography, and visual density settings.
    """
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#a4e6ff",
            on_primary="#003543",
            primary_container="#00d1ff",
            on_primary_container="#00566a",
            secondary="#b7c8e1",
            on_secondary="#213145",
            secondary_container="#3a4a5f",
            on_secondary_container="#a9bad3",
            tertiary="#ceddf6",
            on_tertiary="#233144",
            tertiary_container="#b3c1da",
            on_tertiary_container="#414f64",
            error="#ffb4ab",
            on_error="#690005",
            error_container="#93000a",
            on_error_container="#ffdad6",
            surface="#0b1326",
            on_surface="#dae2fd",
            on_surface_variant="#bbc9cf",
            outline="#859399",
            outline_variant="#3c494e",
            shadow="#000000",
            scrim="#000000",
            inverse_surface="#dae2fd",
            on_inverse_surface="#283044",
            inverse_primary="#00677f",
            surface_tint="#4cd6ff",
            # Surface Container variants from MD3 (Flet 0.84+)
            surface_container_lowest="#060e20",
            surface_container_low="#131b2e",
            surface_container="#171f33",
            surface_container_high="#222a3d",
            surface_container_highest="#2d3449",
        ),
        text_theme=ft.TextTheme(
            headline_large=ft.TextStyle(
                size=32,
                weight=ft.FontWeight.BOLD,
                letter_spacing=-0.5,
                color="#dae2fd",
            ),
            headline_medium=ft.TextStyle(
                size=24,
                weight=ft.FontWeight.BOLD,
                letter_spacing=-0.2,
                color="#dae2fd",
            ),
            headline_small=ft.TextStyle(
                size=18,
                weight=ft.FontWeight.W_500,
                color="#dae2fd",
            ),
            body_large=ft.TextStyle(
                size=16,
                weight=ft.FontWeight.NORMAL,
                color="#dae2fd",
            ),
            body_medium=ft.TextStyle(
                size=14,
                weight=ft.FontWeight.NORMAL,
                color="#dae2fd",
            ),
            label_medium=ft.TextStyle(
                size=12,
                weight=ft.FontWeight.W_500,
                letter_spacing=0.5,
                color="#bbc9cf",
            ),
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
    )
