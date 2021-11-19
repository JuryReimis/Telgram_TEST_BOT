# Обработчики

from aiogram.dispatcher import FSMContext

from db.initialisation import TestsTable
from keyboards.inline_keyboards.choice_right_answer_in_test import create_menu
from keyboards.inline_keyboards.polling_keyboard import create_poll_menu
from main import bot, dp
from handlers.text_handlers.text_handlers import welcome_message
from keyboards.default import menu
from aiogram.types import Message
from config import admin_id
from aiogram.dispatcher.filters import Command
from states.creat_test.creat_test import CreateNameTest
from utils.creat_test.creat_test import Test


async def send_to_admin():
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler(Command("start"))
async def welcome(message: Message):
    await welcome_message(message)


@dp.message_handler(Command("menu"))
async def call_menu(message: Message):
    await message.answer("Чего надо?", reply_markup=menu)


class TestCreator:

    test = None
    iterations = 0
    answers = 1
    questions_text = None
    answer = []

    @staticmethod
    @dp.message_handler(Command("create_test"))
    async def create_test_name(message: Message):
        await message.reply(text="Напиши название теста")
        await CreateNameTest.first()

    @staticmethod
    @dp.message_handler(Command("cancel"), state=[CreateNameTest.Name_is_creating, CreateNameTest.Test_len, CreateNameTest.Question_create, CreateNameTest.Create_answers, CreateNameTest.Right_answer_became])
    async def cancel_creating_test(message: Message, state: FSMContext):
        TestCreator.test = None
        TestCreator.iterations = 0
        TestCreator.answers = 1
        TestCreator.questions_text = None
        TestCreator.answer = []
        await state.finish()
        await message.answer(text="Создание теста отменено!")

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Name_is_creating)
    async def create_test_len(message: Message, state: FSMContext):
        name = str(message.text)
        val = TestsTable("tests.sqlite3")
        val.select_all("tests", "test_name", name)
        if val.cur.fetchone() is None:
            await state.update_data(name=name)
            data = await state.get_data()
            print(data)
            await message.reply(text="Сколько будет вопросов?")
            await message.answer(text="Если вам не нравится что-то из того, что вы ввели, вы можете сбросить создание теста, введя /cancel")
            await CreateNameTest.Test_len.set()
        else:
            await message.reply(text="Тест с таким названием уже существует")
            await message.answer(text="Введите новое название теста")
            await CreateNameTest.Name_is_creating.set()
        val.cur.close()

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Test_len)
    async def first_question(message: Message, state: FSMContext):
        questions_quantity = int(message.text)
        await state.update_data(questions_quantity=questions_quantity)
        data = await state.get_data()
        TestCreator.test = Test(test_name=data["name"], questions_quantity=data["questions_quantity"])
        await message.answer(text="Введите первый вопрос:")
        await CreateNameTest.Question_create.set()

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Question_create)
    async def write_complete(message: Message, state: FSMContext):
        print("Я тут!")
        global questions_text
        global iterations
        questions_text = str(message.text)
        val = TestsTable(database="tests.sqlite3")
        val.select_all(table="questions", param="question_text", note=questions_text)
        question_is_created = val.cur
        if val.cur.fetchone() is None:
            await TestCreator.create_questions(message, state)
        else:
            question = question_is_created.execute(f"""SELECT * from questions WHERE question_text = ?""", (questions_text,)).fetchone()
            val.select_all(table="right_answers", param="question_id", note=question["question_id"])
            right_answer = val.cur.fetchone()["right_answer"]
            await message.reply(text="Уже существует такой вопрос\nВот его параметры: ")
            await message.answer(text=f"Вопрос:{questions_text}\nВарианты ответов: \n{question['answer_1']}\n{question['answer_2']}\n{question['answer_3']}\n{question['answer_4']}")
            await message.answer(text=f"Правильным ответом является: {right_answer}")
            await message.answer(text="Добавить этот вопрос с установленными параметрами?", reply_markup=create_poll_menu(params={"question": question, "right_answer": right_answer}))
        val.cur.close()

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Create_answers)
    async def create_questions(message: Message, state: FSMContext):
        if TestCreator.iterations < TestCreator.test.questions_quantity:
            if TestCreator.answers == 1:
                await message.reply(text="Теперь необходимо задать четыре варианта ответа, один из которых должен быть правильный")
            if TestCreator.answers <= 4:
                await message.answer(text=f"Введите {TestCreator.answers} ответ")
                TestCreator.answers += 1
                await CreateNameTest.Answer_became.set()
            else:
                TestCreator.iterations += 1
                TestCreator.answers = 1
                TestCreator.test.create(questions_text, TestCreator.answer)
                print(TestCreator.iterations)
                await message.answer(text="Какой ответ является верным?", reply_markup=create_menu(TestCreator.answer))
                await CreateNameTest.Right_answer_became.set()
                TestCreator.answer.clear()
        else:
            table = TestsTable("tests.sqlite3")
            print("Out From Iteration")
            questions = TestCreator.test.get_questions()
            table.into_table("tests", (TestCreator.test.default["test_name"], "MAIN_ADMIN", TestCreator.test.questions_quantity, 0, False))  #Первое задействование базы данных уже после ввода всех вопросов
            for question in questions:
                for ans in question.get("answers"):
                    if ans["valid"] is True:
                        right_answer = ans["text"]
                table.into_table(table="questions", notes=[TestCreator.test.default["test_name"], str(question["text"]), str(question["answers"][0]["text"]), str(question["answers"][1]["text"]), str(question["answers"][2]["text"]), str(question["answers"][3]["text"])], right_answer=right_answer)
            await state.finish()
            TestCreator.iterations = 0
            table.cur.close()
            await message.answer("Тест создан!")

    @staticmethod
    @dp.message_handler(state=CreateNameTest.Answer_became)
    async def answer_became(message: Message, state: FSMContext):
        TestCreator.answer.append(message.text)
        print("answer:", TestCreator.answer)
        await TestCreator.create_questions(message=message, state=state)

