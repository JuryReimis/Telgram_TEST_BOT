from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
