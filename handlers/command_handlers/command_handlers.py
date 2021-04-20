# Обработчики
from aiogram.dispatcher import FSMContext

from main import bot, dp
from handlers.text_handlers.text_handlers import welcome_message
from keyboards.default import menu
from aiogram.types import Message
from config import admin_id
from aiogram.dispatcher.filters import Command
from states.creat_test.creat_test import CreateNameTest, CreatQuestions
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


@dp.message_handler(state=CreateNameTest.NameIsCreating)
async def create_test_len(message: Message, state: FSMContext):
    name = str(message.text)
    await state.update_data(name=name)
    data = await state.get_data()
    print(data)
    await message.reply(text="Сколько будет вопросов?")
    await CreateNameTest.next()


@dp.message_handler(state=CreateNameTest.Test_len)
async def ok(message: Message, state: FSMContext):
    questions_quantity = int(message.text)
    await state.update_data(questions_quantity=questions_quantity)
    data = await state.get_data()
    test = Test(test_name=data["name"], questions_quantity=data["questions_quantity"])
    print(data)
    await state.finish()



