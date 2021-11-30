from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline_keyboards.callback_dates import polling_callback, select_test_callback, test_menu_callback
from utils.test_selection.test_selection import create_buttons_pattern

r"""Здесь осуществляется создание клавиатур для выбора чего-либо"""


def create_poll_menu(params: str):
    poll_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data=polling_callback.new(
                    selected=True,
                    context=params
                )),
                InlineKeyboardButton(text="Нет", callback_data=polling_callback.new(
                    selected=False,
                    context=params
                ))
            ]
        ]
    )
    return poll_menu


def create_keyboard_with_random_tests(rows: int, numbers_in_rows: int, data: list):
    r"""В функцию передается количество рядов и количество кнопок в ряду
    Так же в data передается список кортежей каждого теста со всей начинка для кнопок, такая как название теста,
     отображаемое на кнопке и id этого теста в БД
     В переменную buttons возвращается значение функции в виде списка списков с кнопками,
     каждый индекс в списке является рядом в приложении"""
    buttons = create_buttons_pattern(rows=rows, numbers_in_rows=numbers_in_rows, data=data)
    random_poll_menu = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    return random_poll_menu


r"""Создает клавиатуру, которая позволяет осуществить выбор действия над тестами"""
test_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Создать тест",
                                 callback_data=test_menu_callback.new(
                                     choice="create_test"
                                 )),
            InlineKeyboardButton(text="Пройти тест",
                                 callback_data=test_menu_callback.new(
                                     choice="complete_test"
                                 ))
        ],
        [
            InlineKeyboardButton(text="Отмена",
                                 callback_data=test_menu_callback.new(
                                     choice="cancel"
                                 ))
        ]
    ]
)
