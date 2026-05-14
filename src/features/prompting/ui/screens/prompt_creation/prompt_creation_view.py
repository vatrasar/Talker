import flet as ft

@ft.component
def PromptCreationView() -> ft.Container:
    """
    Screen for creating new prompts.

    Purpose: Allows the user to define and configure new prompts for the prompting feature.
    Available Functionalities: Placeholder text display.
    Key UI Elements: Text "prompt_creation screen działa".
    Navigation:
        Navigate From: ProjectPickView (via project card click).
        Navigate To: None (currently).
    Used In: prompting_routes.py.
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("prompt_creation screen działa", size=30, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Go Back", on_click=lambda _: ft.context.page.navigate("/")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )
