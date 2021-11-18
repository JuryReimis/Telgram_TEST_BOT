from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.initialisation import TestsTable, TemporaryTable
from keyboards.inline_keyboards.callback_datas import polling_callback, select_test_callback


def create_poll_menu(params: dict):
    poll_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data=polling_callback.new(
                    selected=True,
                )),
                InlineKeyboardButton(text="Нет", callback_data=polling_callback.new(
                    selected=False,
                ))
            ]
        ]
    )
    return poll_menu


def random_5():
    print("random_5 is started")
    tests = TestsTable("tests.sqlite3")
    poll_menu = InlineKeyboardMarkup(row_width=2)
    temp_table = TemporaryTable()
    for i in range(5):
        print("i=", i)
        tests.select_random_str()
        random_str = tests.cur.fetchone()
        temp_table.into_table(random_str["test_id"])
        button = InlineKeyboardButton(text=random_str["test_name"], callback_data=select_test_callback.new(selected=random_str["test_id"]))
        poll_menu.insert(button)
    temp_table.close_connection()
    return poll_menu
