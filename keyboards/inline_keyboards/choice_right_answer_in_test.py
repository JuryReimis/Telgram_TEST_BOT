from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_keyboards.callback_datas import selected_answer_callback


def choice_answer_menu(answer, flag=None):
    if flag == "performed":
        answers = [i["text"] for i in answer]
    else:
        answers = answer
    choice_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=answers[0], callback_data=selected_answer_callback.new(
                    selected=0
                )),
                InlineKeyboardButton(text=answers[1], callback_data=selected_answer_callback.new(
                    selected=1
                )),
            ],
            [
                InlineKeyboardButton(text=answers[2], callback_data=selected_answer_callback.new(
                    selected=2
                )),
                InlineKeyboardButton(text=answers[3], callback_data=selected_answer_callback.new(
                    selected=3
                )),
            ]
        ]
    )
    return choice_menu
