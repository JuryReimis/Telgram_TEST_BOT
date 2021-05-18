from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_keyboards.callback_datas import create_right_answer_callback


def create_menu(answer):
    choice_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=answer[0], callback_data=create_right_answer_callback.new(
                    selected=0
                )),
                InlineKeyboardButton(text=answer[1], callback_data=create_right_answer_callback.new(
                    selected=1
                )),
            ],
            [
                InlineKeyboardButton(text=answer[2], callback_data=create_right_answer_callback.new(
                    selected=2
                )),
                InlineKeyboardButton(text=answer[3], callback_data=create_right_answer_callback.new(
                    selected=3
                )),
            ]
        ]
    )
    return choice_menu
