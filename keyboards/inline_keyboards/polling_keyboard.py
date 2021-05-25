from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_keyboards.callback_datas import polling_callback, select_test_callback


def create_poll_menu(params: dict):
    poll_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data=polling_callback.new(
                    selected=True,
                    context=params
                )),
                InlineKeyboardButton(text="Нет", callback_data=polling_callback.new(
                    selected=False
                ))
            ]
        ]
    )


def random_5():
    poll_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="", callback_data=select_test_callback.new(
                    selected=""
                ))
            ]
        ]
    )
