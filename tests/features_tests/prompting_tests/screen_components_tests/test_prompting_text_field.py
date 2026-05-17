import flet as ft
from unittest.mock import patch, MagicMock, PropertyMock
from features.prompting.domain.enums.file_system_item_type import FileSystemItemType
from features.prompting.domain.models.file_system_item_for_prompt import FileSystemItemForPrompt
import pytest
from features.prompting.domain.models.item_in_sorted_list import ItemInSortedList
from features.prompting.domain.services.prompting_creation_service import PromptingCreationService
from features.prompting.domain.use_cases.merge_prompt_text_use_case import MergePromptTextUseCase
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
    use_case = MergePromptTextUseCase()
    vm = PromptingTextFieldViewModel(
        prompting_creation_service=service,
        merge_prompt_text_use_case=use_case,
    )
    
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
    
    use_case = MergePromptTextUseCase()
    vm = PromptingTextFieldViewModel(
        prompting_creation_service=service,
        merge_prompt_text_use_case=use_case,
    )
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


@pytest.mark.asyncio
async def test_merge_prompt_text_use_case() -> None:
    """
    Verifies that MergePromptTextUseCase merges words backwards until it hits a file system item.
    """
    use_case = MergePromptTextUseCase()
    
    file_item = FileSystemItemForPrompt(name="main.py", path="/workspace/main.py", type=FileSystemItemType.FILE)
    items = [
        ItemInSortedList(index=0, value="word1"),
        ItemInSortedList(index=1, value="word2"),
        ItemInSortedList(index=2, value=file_item),
        ItemInSortedList(index=3, value="word3"),
        ItemInSortedList(index=4, value="word4"),
    ]
    
    text, indices = await use_case.execute(items)
    assert text == "word3 word4"
    assert indices == [3, 4]

    text2, indices2 = await use_case.execute([ItemInSortedList(index=0, value=file_item)])
    assert text2 == ""
    assert indices2 == []

    items3 = [
        ItemInSortedList(index=0, value="word1"),
        ItemInSortedList(index=1, value="word2"),
    ]
    text3, indices3 = await use_case.execute(items3)
    assert text3 == "word1 word2"
    assert indices3 == [0, 1]


def test_replace_merged_text_in_service() -> None:
    """
    Verifies that replace_merged_text successfully filters out merged items,
    splits and appends the new text, and correctly recalculates consecutive indices.
    """
    service = PromptingCreationService()
    service.addNewText("word1 word2")
    file_item = FileSystemItemForPrompt(name="main.py", path="/workspace/main.py", type=FileSystemItemType.FILE)
    service._items.append(ItemInSortedList(index=2, value=file_item))
    service.addNewText("word3 word4")

    items_before = service.get_items()
    assert len(items_before) == 5
    assert items_before[0].value == "word1"
    assert items_before[1].value == "word2"
    assert items_before[2].value == file_item
    assert items_before[3].value == "word3"
    assert items_before[4].value == "word4"

    service.replace_merged_text("edited word5", [3, 4])

    items_after = service.get_items()
    assert len(items_after) == 5
    assert items_after[0].value == "word1"
    assert items_after[0].index == 0
    assert items_after[1].value == "word2"
    assert items_after[1].index == 1
    assert items_after[2].value == file_item
    assert items_after[2].index == 2
    assert items_after[3].value == "edited"
    assert items_after[3].index == 3
    assert items_after[4].value == "word5"
    assert items_after[4].index == 4


@pytest.mark.asyncio
async def test_view_model_focus_blur_editing_flow() -> None:
    """
    Verifies that the ViewModel handles the focus/blur merging and commit flow correctly.
    """
    service = PromptingCreationService()
    service.addNewText("hello world")
    
    use_case = MergePromptTextUseCase()
    vm = PromptingTextFieldViewModel(
        prompting_creation_service=service,
        merge_prompt_text_use_case=use_case,
    )
    vm.update_props("Label")
    
    assert len(vm.state.items) == 2
    assert vm.state.value == ""
    
    await vm.handle_focus()
    assert vm.state.value == "hello world"
    assert len(vm.state.items) == 0
    
    vm.update_text("hello edited universe")
    assert vm.state.value == "hello edited universe"
    
    await vm.finish_editing()
    assert vm.state.value == ""
    assert len(vm.state.items) == 3
    assert vm.state.items[0].value == "hello"
    assert vm.state.items[1].value == "edited"
    assert vm.state.items[2].value == "universe"

