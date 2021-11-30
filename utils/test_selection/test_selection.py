from random import sample
from aiogram.types import InlineKeyboardButton, CallbackQuery
from db.initialisation import TestsTable
from keyboards.inline_keyboards.callback_dates import select_test_callback

r"""Утилита выполняет необходимые действия при прохождении теста"""


def create_buttons_pattern(rows: int, numbers_in_rows: int, data) -> list:
    r"""Функция создает каркас для клавиатуры с случайными кнопками
    Возвращает список списков кнопок, где первый индекс означает номер ряда кнопок, а второй положение в ряду кнопок"""
    buttons = [[] for _ in range(rows)]
    data_index = 0
    for row in range(rows):
        for _ in range(numbers_in_rows):
            if data_index >= len(data):
                return buttons
            buttons[row].append(InlineKeyboardButton(text=data[data_index].test_name,
                                                     callback_data=select_test_callback.new(
                                                         selected_id=str(data[data_index].test_id)
                                                     )))
            data_index += 1
    return buttons


def get_random_tests_data(count: int, db: TestsTable):
    r"""Функция для получения случайного количества тестов из БД"""
    data: list = db.get_all_tests()
    if count > len(data):
        count = len(data)
    return sample(data, k=count)


async def answers_output(call: CallbackQuery, questions: list, user_answers: dict):
    r"""Функция для обработки результатов тестирования, сравнивает ответы пользователя с правильными ответами из БД"""
    await call.message.answer(text="Ваши ответы:")
    count_right_answers = 0
    for question in questions:
        right_answers = ""
        for answer in question["answers"]:
            if answer["valid"] is True:
                right_answers = str(answer["text"])
        count_right_answers += 1 if user_answers[question["text"]] == right_answers else 0
        text = str(user_answers[question["text"]])+"-"+("Правильно" if user_answers[question["text"]] == right_answers else f"Неверно, правильный ответ: {right_answers}")
        await call.message.answer(text=text)
    await call.message.answer(text=f"Итого тест пройден на {int(count_right_answers/len(questions)*100)}%")
