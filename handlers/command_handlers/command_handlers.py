# Обработчики
import pprint

from aiogram.dispatcher import FSMContext

from keyboards.inline_keyboards.callback_datas import create_right_answer_callback
from keyboards.inline_keyboards.choice_right_answer_in_test import create_menu
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


@dp.message_handler(Command("create_test"))
async def create_test_name(message: Message):
    await message.reply(text="Напиши название теста")
    await CreateNameTest.first()


@dp.message_handler(state=CreateNameTest.Name_is_creating)
async def create_test_len(message: Message, state: FSMContext):
    name = str(message.text)
    await state.update_data(name=name)
    data = await state.get_data()
    print(data)
    await message.reply(text="Сколько будет вопросов?")
    await CreateNameTest.next()


test = None
iterations = 0
answers = 1
questions_text = None
answer = []


@dp.message_handler(state=CreateNameTest.Test_len)
async def first_question(message: Message, state: FSMContext):
    questions_quantity = int(message.text)
    await state.update_data(questions_quantity=questions_quantity)
    data = await state.get_data()
    global test
    test = Test(test_name=data["name"], questions_quantity=data["questions_quantity"])
    print(test.default)
    await message.answer(text="Введите первый вопрос:")
    await CreateNameTest.next()


@dp.message_handler(state=CreateNameTest.Question_create)
async def write_complete(message: Message, state: FSMContext):
    print("Я тут!")
    global questions_text
    global iterations
    iterations += 1
    questions_text = message.text
    await create_questions(message, state)


@dp.message_handler(state=CreateNameTest.Create_answers)
async def create_questions(message: Message, state: FSMContext):
    global test
    global iterations
    global answers
    global questions_text
    if iterations <= test.questions_quantity:
        if answers == 1:
            await message.reply(text="Теперь необходимо задать четыре варианта ответа, один из которых должен быть правильный")
        if answers <= 4:
            await message.answer(text=f"Введите {answers} ответ")
            answers += 1
            await CreateNameTest.Answer_became.set()
        else:
            answers = 1
            test.create(questions_text, answer)
            await message.answer(text="Какой ответ является верным?", reply_markup=create_menu(answer))
            await CreateNameTest.Right_answer_became.set()
            answer.clear()
    else:
        await state.finish()


@dp.message_handler(state=CreateNameTest.Answer_became)
async def answer_became(message: Message, state: FSMContext):
    global answer
    answer.append(message.text)
    print("answer:", answer)
    await create_questions(message=message, state=state)
