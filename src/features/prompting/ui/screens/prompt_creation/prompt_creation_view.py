import flet as ft
import urllib.parse
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel

@ft.component
def PromptCreationView() -> ft.Container:
    """
    Screen for creating new prompts.

    Purpose: Allows the user to define and configure new prompts for the prompting feature.
    Available Functionalities: Displays open project information.
    Key UI Elements: Project name and path display.
    Navigation:
        Navigate From: ProjectPickView (via project card click).
        Navigate To: None (currently).
    Used In: prompting_routes.py.
    """
    page: ft.Page = ft.context.page
    di = page.session.store.get("di_container")
    vm: PromptCreationViewModel = ft.use_memo(di.build_prompt_creation_view_model, [])
    state, _ = ft.use_state(vm.state)
    
    params = ft.use_route_params()
    
    def on_mount():
        name = urllib.parse.unquote(params.get("project_name", ""))
        path = urllib.parse.unquote(params.get("project_path", ""))
        vm.set_project_info(name, path)

    ft.use_effect(on_mount, [params])

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Prompt Creation Screen", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(f"Project Name: {state.project_name}", size=20),
                ft.Text(f"Project Path: {state.project_path}", size=16, italic=True),
                ft.ElevatedButton("Go Back", on_click=lambda _: ft.context.page.navigate("/")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )
