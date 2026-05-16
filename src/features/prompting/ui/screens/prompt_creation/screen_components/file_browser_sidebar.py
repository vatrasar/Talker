import flet as ft
from features.prompting.domain.models.file_system_item import FileSystemItem
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from features.prompting.ui.screens.prompt_creation.prompt_creation_view_model import PromptCreationViewModel

@ft.component
def FileBrowserSidebar(vm: PromptCreationViewModel) -> ft.Container:
    """
    Sidebar component for browsing project files.

    Purpose: Displays a tree structure of the current project's files and folders.
    Key UI Elements: Folder tree with manual expansion control.
    Used In: PromptCreationView.
    """
    state, _ = ft.use_state(vm.state)

    def build_tree_controls(items: list[FileSystemItem]) -> list[ft.Control]:
        return [
            FileBrowserItem(
                item=item,
                vm=vm,
                children=build_tree_controls(item.children) if item.type == FileSystemItemType.FOLDER else None
            )
            for item in items
        ]

    header_icon = ft.Icon(ft.Icons.ACCOUNT_TREE_ROUNDED, color=ft.Colors.PRIMARY)
    header_text = ft.Text("Project Files", weight=ft.FontWeight.BOLD, size=18)
    header_row = ft.Row(
        controls=[
            header_icon, 
            header_text, 
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    divider = ft.Divider(height=20, thickness=1)
    
    tree_list = ft.Column(
        controls=build_tree_controls(state.file_system_tree) if not state.is_loading_files else [],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
        visible=not state.is_loading_files
    )
    
    loading_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.ProgressRing(),
                alignment=ft.Alignment.CENTER,
                expand=True
            ),
            ft.Text("Loading files...", size=14, color=ft.Colors.OUTLINE)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        visible=state.is_loading_files
    )

    return ft.Container(
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        width=state.sidebar_width,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border_radius=16,
        padding=15,
        content=ft.Column(
            controls=[
                header_row,
                divider,
                tree_list,
                loading_content,
            ],
            expand=True
        )
    )


@ft.component
def FileBrowserItem(item: FileSystemItem, vm: PromptCreationViewModel, children: list = None) -> ft.Column | ft.Container:
    state, _ = ft.use_state(vm.state)
    is_expanded = item.path in state.expanded_folders
    is_hovered, set_is_hovered = ft.use_state(False)

    async def toggle_expand(e: ft.ControlEvent):
        await vm.toggle_folder(item.path)

    def on_hover(e: ft.ControlEvent):
        set_is_hovered(e.data == "true")

    icon_type = (ft.Icons.FOLDER_OPEN if is_expanded else ft.Icons.FOLDER) if children else ft.Icons.INSERT_DRIVE_FILE_OUTLINED
    icon_color = ft.Colors.PRIMARY if children else ft.Colors.OUTLINE
    item_icon = ft.Icon(icon_type, color=icon_color, size=18)
    
    item_text = ft.Text(
        item.name, 
        size=13, 
        color=ft.Colors.PRIMARY if is_expanded else ft.Colors.ON_SURFACE,
        weight=ft.FontWeight.W_500 if is_expanded else None,
        no_wrap=True,
    )
    
    expand_btn_controls = []
    if children:
        expand_btn_controls.append(
            ft.IconButton(
                icon=ft.Icons.REMOVE_CIRCLE_OUTLINE if is_expanded else ft.Icons.ADD_CIRCLE_OUTLINE,
                icon_size=16,
                icon_color=ft.Colors.PRIMARY_CONTAINER,
                on_click=toggle_expand,
                width=24,
                height=24,
                style=ft.ButtonStyle(padding=ft.Padding.all(0)),
            )
        )
        
    row_content = ft.Row(
        controls=[item_icon, item_text, *expand_btn_controls],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    item_row = ft.Container(
        content=row_content,
        padding=ft.Padding.only(left=4, top=2, right=4, bottom=2),
        border_radius=8,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST if is_hovered else None,
        on_hover=on_hover,
    )

    if not children:
        return item_row

    children_container = ft.Container(
        content=ft.Column(
            controls=children,
            spacing=0,
        ),
        padding=ft.Padding.only(left=10),
        margin=ft.Margin.only(left=10),
        border=ft.Border(left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        height=None if is_expanded else 0,
        width=None if is_expanded else 0,
        opacity=1 if is_expanded else 0,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    return ft.Column(
        controls=[
            item_row,
            children_container
        ],
        spacing=0
    )
