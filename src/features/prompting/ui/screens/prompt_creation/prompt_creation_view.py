import flet as ft
import urllib.parse
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel
from features.prompting.ui.screens.prompt_creation.screen_components.file_browser_sidebar import FileBrowserSidebar
from features.prompting.ui.screens.prompt_creation.screen_components.prompt_editor import PromptEditor
from features.prompting.ui.screens.prompt_creation.screen_components.prompt_settings_sidebar import PromptSettingsSidebar

@ft.component
def PromptCreationView() -> ft.Container:
    """
    Screen for creating new prompts.

    Purpose: Allows the user to define and configure new prompts for the prompting feature.
    Available Functionalities: Folder navigation, text translation, and whisper settings.
    Key UI Elements: Folder tree, dual text fields, action buttons, settings sidebar.
    Navigation:
        Navigate From: ProjectPickView (via project card click).
        Navigate To: None (currently).
    Used In: prompting_routes.py.
    """
    page: ft.Page = ft.context.page
    di = page.session.store.get("di_container")
    vm: PromptCreationViewModel = ft.use_memo(di.build_prompt_creation_view_model, [])
    
    params = ft.use_route_params()
    
    async def load_project_data():
        name = urllib.parse.unquote(params.get("project_name", ""))
        path = urllib.parse.unquote(params.get("project_path", ""))
        await vm.set_project_info(name, path)

    def on_mount():
        page.run_task(load_project_data)

    ft.use_effect(on_mount, [params])

    return ft.Container(
        content=ft.Row(
            controls=[
                FileBrowserSidebar(vm=vm),
                PromptEditor(vm=vm),
                PromptSettingsSidebar(),
            ],
            expand=True,
            spacing=0
        ),
        padding=15,
        expand=True,
        bgcolor=ft.Colors.SURFACE,
    )
