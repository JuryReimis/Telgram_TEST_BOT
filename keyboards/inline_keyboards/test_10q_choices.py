from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback_dates import test_callback


def creat_keyboard(responses) -> InlineKeyboardMarkup:
    response_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=responses[0], callback_data=test_callback.new(response=1)),
                InlineKeyboardButton(text=responses[1], callback_data=test_callback.new(response=2))
            ],
            [
                InlineKeyboardButton(text=responses[2], callback_data=test_callback.new(response=3)),
                InlineKeyboardButton(text=responses[3], callback_data=test_callback.new(response=4))
            ],
        ]
    )
    return response_menu
