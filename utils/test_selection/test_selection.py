from random import choices

from aiogram.types import InlineKeyboardButton
from db.initialisation import TestsTable
from keyboards.inline_keyboards.callback_datas import select_test_callback


def create_buttons_pattern(rows: int, numbers_in_rows: int, data) -> list:
    buttons = [[] for _ in range(rows)]
    data_index = 0
    for row in range(rows):
        for _ in range(numbers_in_rows):
            if data_index >= len(data):
                return buttons
            buttons[row].append(InlineKeyboardButton(text=data[data_index]["test_name"],
                                                     callback_data=select_test_callback.new(
                                                         selected_id=str(data[data_index]["test_id"])
                                                     )))
            data_index += 1
    return buttons


def get_random_tests_data(count: int, db: TestsTable):
    data: list = db.get_all_tests()
    return choices(data, k=count)
