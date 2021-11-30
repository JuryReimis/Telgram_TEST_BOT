from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline_keyboards.callback_dates import insult_callback


def insult():
    r"""Функция создает клавиатуру для выбора силы оскорбления
    Возвращает клавиатуру"""
    choice_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Очень легкое оскорбление", callback_data=insult_callback.new(
                    insult_force=1
                )),
                InlineKeyboardButton(text="Легкое оскорбление", callback_data=insult_callback.new(
                    insult_force=2
                ))
            ],
            [
                InlineKeyboardButton(text="Обидное оскорбление", callback_data=insult_callback.new(
                    insult_force=3
                ))
            ],
            [
                InlineKeyboardButton(text="Не надо, я передумал", callback_data="cancel")
            ]
        ]
    )
    return choice_menu
