import flet as ft
from unittest.mock import patch, MagicMock, PropertyMock
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from features.prompting.domain.models.file_system_item_for_prompt import FileSystemItemForPrompt
from features.prompting.domain.models.item_in_sorted_list import ItemInSortedList
from features.prompting.domain.services.prompting_creation_service import PromptingCreationService
from features.prompting.ui.screens.prompt_creation.screen_components.prompting_text_field.prompting_text_field_view import PromptingTextField
from features.prompting.ui.screens.prompt_creation.screen_components.prompting_text_field.prompting_text_field_view_model import PromptingTextFieldViewModel

def test_prompting_creation_service_behavior() -> None:
    """
    Verifies that PromptingCreationService correctly splits, indexes, tracks typing,
    and returns deep copies of its items list.
    """
    service = PromptingCreationService()
    
    # 1. Test update
    service.update("hello")
    assert service.current_text == "hello"
    
    # 2. Test addNewText
    service.addNewText("hello world test")
    items = service.get_items()
    assert len(items) == 3
    assert items[0].index == 0
    assert items[0].value == "hello"
    assert items[1].index == 1
    assert items[1].value == "world"
    assert items[2].index == 2
    assert items[2].value == "test"
    
    # Ensure current text buffer is cleared
    assert service.current_text == ""
    
    # 3. Test deep copy
    items[0].value = "mutated"
    fresh_items = service.get_items()
    assert fresh_items[0].value == "hello"  # Unmutated!

    # 4. Test empty and whitespace-only text
    service.addNewText("")
    assert len(service.get_items()) == 3  # Still 3!
    assert service.current_text == ""

    service.addNewText("   ")
    assert len(service.get_items()) == 3  # Still 3!
    assert service.current_text == ""


def test_prompting_text_field_view_model() -> None:
    """
    Verifies that PromptingTextFieldViewModel correctly interacts with the service
    and updates reactive state properties.
    """
    service = PromptingCreationService()
    vm = PromptingTextFieldViewModel(prompting_creation_service=service)
    
    # 1. Test update_props
    vm.update_props("Prompt Label")
    assert vm.state.label == "Prompt Label"
    
    # 2. Test update_text
    vm.update_text("typing some text")
    assert vm.state.value == "typing some text"
    assert service.current_text == "typing some text"
    
    # 3. Test add_text_to_prompt
    vm.add_text_to_prompt()
    assert vm.state.value == ""
    assert len(vm.state.items) == 3
    assert vm.state.items[0].value == "typing"
    assert vm.state.items[1].value == "some"
    assert vm.state.items[2].value == "text"


# Define the mock structures
mock_page = MagicMock()
mock_di = MagicMock()

@patch("flet.controls.context.Context.page", new_callable=PropertyMock)
@patch("flet.use_state", side_effect=lambda x: (x, lambda y: None))
@patch("flet.use_effect", side_effect=lambda fn, deps: fn())
@patch("flet.use_memo", side_effect=lambda fn, deps: fn())
def test_prompting_text_field_rendering(mock_use_memo: MagicMock, mock_use_effect: MagicMock, mock_use_state: MagicMock, mock_page_prop: PropertyMock) -> None:
    """
    Verifies that PromptingTextField component correctly loops through state items
    and renders standard Text controls for words and premium Button chips for file items.
    """
    service = PromptingCreationService()
    # Add one text word and one FileSystemItemForPrompt
    service.addNewText("hello")
    file_item = FileSystemItemForPrompt(name="main.py", path="/workspace/main.py", type=FileSystemItemType.FILE)
    service._items.append(ItemInSortedList(index=1, value=file_item))
    
    vm = PromptingTextFieldViewModel(prompting_creation_service=service)
    vm.update_props("Label")
    
    mock_di.build_prompting_text_field_view_model.return_value = vm
    mock_page.session.store.get.return_value = mock_di
    mock_page_prop.return_value = mock_page
    
    # Act
    component = PromptingTextField.__component_impl__(label="Label", min_lines=5)
    
    # Assert
    assert isinstance(component, ft.Container)
    
    stack = component.content
    assert isinstance(stack, ft.Stack)
    
    border_container = stack.controls[0]
    inner_container = border_container.content
    
    row = inner_container.content
    assert isinstance(row, ft.Row)
    assert row.wrap is True
    
    # Expected: 1 Text control (word) + 1 Chip Container (file) + 1 TextField (trailing) = 3 controls
    assert len(row.controls) == 3
    
    # First: word Text control
    assert isinstance(row.controls[0], ft.Text)
    assert row.controls[0].value == "hello"
    
    # Second: file chip Container
    assert isinstance(row.controls[1], ft.Container)
    chip_row = row.controls[1].content
    assert isinstance(chip_row, ft.Row)
    icon_ctrl = chip_row.controls[0]
    text_ctrl = chip_row.controls[1]
    assert isinstance(icon_ctrl, ft.Icon)
    assert icon_ctrl.icon == ft.Icons.INSERT_DRIVE_FILE_ROUNDED
    assert isinstance(text_ctrl, ft.Text)
    assert text_ctrl.value == "main.py"
    
    # Third: TextField input
    assert isinstance(row.controls[2], ft.TextField)
