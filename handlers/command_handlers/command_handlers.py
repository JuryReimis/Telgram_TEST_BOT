# Обработчики команд
import string

from aiogram.dispatcher import FSMContext

from db.initialisation import TestsTable
from keyboards.inline_keyboards.choice_right_answer_in_test import choice_answer_menu
from keyboards.inline_keyboards.polling_keyboard import create_poll_menu, test_choice, create_keyboard_with_random_tests
from main import bot, dp
from handlers.text_handlers.text_handlers import welcome_message
from keyboards.default import menu
from aiogram.types import Message
from config import admin_id
from aiogram.dispatcher.filters import Command
from states.creat_test.create_test import CreateNameTest
from states.start_test.start_test import StartTest
from utils.create_test.create_test import Test
from utils.test_selection.test_selection import get_random_tests_data
from collections import namedtuple


class TestCreator:
    r"""Класс для обработки всех комманд, связанных с созданием теста, а так же для обработки самого создания"""
    test: Test  # Экземпляр класса Тест
    question_registered: int  # Сколько вопросов уже зарегистрировано
    answers_received: int  # Получено ответов
    question_text: str  # Текст записанного вопроса
    answers_list: list = []  # Список ответов на записанный вопрос
    question: namedtuple  # Словарь вопросов
    db_connection: TestsTable  # Коннект к базе данных

    @staticmethod
    @dp.message_handler(Command("cancel"),
                        state=[CreateNameTest.Name_is_creating, CreateNameTest.Get_tests_length,
                               CreateNameTest.Question_selection,
                               CreateNameTest.Create_answers, CreateNameTest.Right_answer_became])
    async def cancel_creating_test(message: Message, state: FSMContext):
        r"""Метод-хэндлер отменяет создание теста, улавливая комманду /cancel"""
        TestCreator.test = None
        TestCreator.question_registered = 0
        TestCreator.answers_received = 1
        TestCreator.question_text = None
        TestCreator.answers_list = []
        await state.finish()
        await message.answer(text="Создание теста отменено!")

    @staticmethod
    @dp.message_handler(Command("create_test"))
    async def create_test_name(message: Message):
        r"""Улавливает комманду /create_test"""
        await message.reply(text="Напиши название теста")
        TestCreator.db_connection = TestsTable(database="tests")
        TestCreator.question_registered = 0
        TestCreator.answers_received = 1
        TestCreator.question_text = ""
        TestCreator.answers_list = []
        await CreateNameTest.Name_is_creating.set()

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Name_is_creating)
    async def create_test_len(message: Message, state: FSMContext):
        r"""Фиксирует название теста, отправляет на проверку на дубликаты"""
        name = str(message.text)
        TestCreator.db_connection.select_all("tests", "test_name", name)
        if TestCreator.db_connection.curs.fetchone() is None:
            await state.update_data(name=name)
            await message.reply(text="Сколько будет вопросов?")
            await message.answer(
                text="""Если вам не нравится что-то из того, что вы ввели, вы можете сбросить создание теста,
введя /cancel""")
            await CreateNameTest.Get_tests_length.set()
        else:
            await message.reply(text="Тест с таким названием уже существует")
            await message.answer(text="Введите новое название теста")
            await CreateNameTest.Name_is_creating.set()

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Get_tests_length)
    async def registration_tests_length(message: Message, state: FSMContext):
        r"""Получает длину теста, проверяет, является ли полученное сообщение числом"""
        flag = True
        for digit in message.text:
            if digit not in string.digits:
                flag = False
        if flag:
            questions_quantity = int(message.text)  # Полученную из телеграма строку превращаем в число
            await state.update_data(questions_quantity=questions_quantity)
            data = await state.get_data()
            TestCreator.db_connection.into_table(table="tests",
                                                 notes=(data["name"], "MAIN_ADMIN", questions_quantity, 0, False))
            TestCreator.test = Test(test_name=data["name"], questions_quantity=data["questions_quantity"])
            await message.answer(text="Введите первый вопрос:")
            await CreateNameTest.Question_selection.set()
        else:
            await message.answer(text="Введено не число, повторите ввод")

    @staticmethod
    @dp.message_handler(
        state=CreateNameTest.Question_selection)  # Сюда попадают все вопросы, которые вводятся при фиксации вопросов
    async def question_selection(message: Message, state: FSMContext):
        r"""Метод обрабатывает вопрос, который ввел пользователь, проверяет его наличие в БД и, в случае наличия,
        предлагает добавить существующий вопрос в тест"""
        TestCreator.question_text = str(message.text)
        TestCreator.db_connection.select_all(table="questions", param="question_text", note=TestCreator.question_text)
        if TestCreator.db_connection.curs.fetchone() is None:  # Проверка на наличие записи в БД
            await TestCreator.create_questions(message, state)
        else:
            TestCreator.db_connection.select_all(table="questions", param="question_text",
                                                 note=TestCreator.question_text)
            TestCreator.question = TestCreator.db_connection.curs.fetchone()
            TestCreator.db_connection.select_all(table="right_answers", param="question_id",
                                                 note=TestCreator.question.question_id)
            right_answer = TestCreator.db_connection.curs.fetchone().right_answer
            await message.reply(text="Уже существует такой вопрос\nВот его параметры: ")
            await message.answer(
                text=f"""Вопрос:{TestCreator.question_text}
            Варианты ответов: 
            {TestCreator.question.answer_1}
            {TestCreator.question.answer_2}
            {TestCreator.question.answer_3}
            {TestCreator.question.answer_4}""")
            await message.answer(text=f"Правильным ответом является: {right_answer}")
            await message.answer(text="Добавить этот вопрос с установленными параметрами?",
                                 reply_markup=create_poll_menu(params="question_selection"))

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Create_answers)
    async def create_questions(message: Message, state: FSMContext):
        r"""Метод принимает текст вопроса, предлагает создать ответы и проверяет количество этих ответов в цикле
        Так же при фиксации необходимого числа вопросов происходит завершение создания теста и
        запись всего необходимогов БД"""
        if TestCreator.question_registered < TestCreator.test.questions_quantity:
            if TestCreator.answers_received == 1:
                await message.reply(
                    text="Теперь необходимо задать четыре варианта ответа, один из которых должен быть правильный")
            if TestCreator.answers_received <= 4:
                await message.answer(text=f"Введите {TestCreator.answers_received} ответ")
                TestCreator.answers_received += 1
                await CreateNameTest.Answer_became.set()
            else:
                TestCreator.test.create(question_text=TestCreator.question_text, answers=TestCreator.answers_list)
                await message.answer(text="Какой ответ является верным?",
                                     reply_markup=choice_answer_menu(TestCreator.answers_list))
                await CreateNameTest.Right_answer_became.set()
                TestCreator.answers_list.clear()
                TestCreator.answers_received = 1
        else:
            right_answer = None
            questions = TestCreator.test.get_questions()
            for question in questions:
                for ans in question.get("answers"):
                    if ans["valid"] is True:
                        right_answer = ans["text"]
                TestCreator.db_connection.into_table(table="questions",
                                                     notes=[str(question["text"]), str(question["answers"][0]["text"]),
                                                            str(question["answers"][1]["text"]),
                                                            str(question["answers"][2]["text"]),
                                                            str(question["answers"][3]["text"])],
                                                     right_answer=right_answer)
            await state.finish()
            TestCreator.question_registered = 0
            TestCreator.db_connection.save_tables()
            TestCreator.db_connection.curs.close()
            await message.answer("Тест создан!")

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Answer_became)  # Сюда попадают полученные от пользователя ответы
    async def answer_became(message: Message, state: FSMContext):
        r"""Метод для обработки введенных пользователем ответов"""
        TestCreator.answers_list.append(message.text)
        await TestCreator.create_questions(message=message, state=state)


class TestShower:
    db_connection: TestsTable

    @staticmethod
    @dp.message_handler(Command("start_test"))
    async def start_complete_test(message: Message):
        TestShower.db_connection = TestsTable(database="tests")
        tests_data = get_random_tests_data(count=6, db=TestShower.db_connection)
        print("tests_data", tests_data)
        await message.answer(text="Выберите тест, который хотите пройти:",
                             reply_markup=create_keyboard_with_random_tests(rows=2, numbers_in_rows=3, data=tests_data))
        TestShower.db_connection.curs.close()

    @staticmethod
    @dp.message_handler(state=StartTest.Test_choice)
    async def get_question(message: Message, state: FSMContext):
        pass


async def send_to_admin():
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler(Command("start"))
async def welcome(message: Message):
    await welcome_message(message)


@dp.message_handler(Command("menu"))
async def call_menu(message: Message):
    await message.answer("Чего надо?", reply_markup=menu)


@dp.message_handler(Command("test_menu"))
async def open_test_menu(message: Message):
    await message.answer(text="Выберите, что вы хотите?", reply_markup=test_choice)
