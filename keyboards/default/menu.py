from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

r"""Обычная клавиатура, которая появляется при вводе команды /menu"""
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Привет"),
            KeyboardButton(text="Пришли мне приветствие")
        ],
        [
            KeyboardButton(text="Хочу получить оскорбления на выбор")
        ],
        [
            KeyboardButton(text="Тесты")
        ],
        [
            KeyboardButton(text="Спасибо")
        ],
    ],
    resize_keyboard=True
)
